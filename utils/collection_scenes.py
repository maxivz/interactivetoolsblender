
import bpy
from mathutils import Matrix, Quaternion

# ============================================================
# CONFIGURATION
# ============================================================

WORLD_SCENE_NAME = "World_Aligned"
RIG_SCENE_NAME = "Rig"

LOCATOR_COLLECTION_NAME = "__Collection_Locators__"
LOCATOR_PREFIX = "__LOCATOR__"

ASSET_PREFIX = "WA__"
CONTROL_PREFIX = "CTRL__"

GENERATED_KEY = "_collection_pipeline_generated"
LOCATOR_KEY = "_collection_locator_for"
SOURCE_KEY = "_collection_pipeline_source"

# Stored on every source collection.
PROP_LOCATION = "_locator_location"
PROP_ROTATION = "_locator_rotation_quaternion"
PROP_SCALE = "_locator_scale"


# ============================================================
# COLLECTION / SCENE UTILITIES
# ============================================================

def get_or_create_collection(parent, name):
    collection = bpy.data.collections.get(name)

    if collection is None:
        collection = bpy.data.collections.new(name)

    if collection.name not in parent.children:
        parent.children.link(collection)

    return collection


def remove_generated_scenes_and_data():
    """Delete previous generated output, never source collections."""

    # Remove generated scenes first.
    for name in (WORLD_SCENE_NAME, RIG_SCENE_NAME):
        scene = bpy.data.scenes.get(name)
        if scene is not None:
            bpy.data.scenes.remove(scene, do_unlink=True)

    # Remove objects marked as generated.
    for obj in list(bpy.data.objects):
        if obj.get(GENERATED_KEY, False):
            bpy.data.objects.remove(obj, do_unlink=True)

    # Remove generated collections, deepest first.
    generated = [
        collection
        for collection in bpy.data.collections
        if collection.get(GENERATED_KEY, False)
    ]

    for collection in generated:
        bpy.data.collections.remove(collection, do_unlink=True)


def create_scene(name):
    scene = bpy.data.scenes.new(name)
    return scene


def get_source_collections(scene):
    """
    Collect every collection linked below the source scene root.
    The locator collection and previously generated collections
    are excluded.
    """

    result = []
    visited = set()

    def visit(collection):
        if collection == bpy.data.collections.get(
            LOCATOR_COLLECTION_NAME
        ):
            return

        if collection.get(GENERATED_KEY, False):
            return

        pointer = collection.as_pointer()
        if pointer in visited:
            return

        visited.add(pointer)
        result.append(collection)

        for child in collection.children:
            visit(child)

    for collection in scene.collection.children:
        visit(collection)

    return result


def get_collection_parent_map(scene, collections):
    """
    Record the first parent encountered for each collection.
    Blender collections can have multiple parents; a rig hierarchy
    must choose one parent per control.
    """

    allowed = set(collections)
    parent_map = {}

    def visit(parent, visited):
        pointer = parent.as_pointer()

        if pointer in visited:
            return
        visited.add(pointer)

        for child in parent.children:
            if child not in allowed:
                continue

            if child not in parent_map:
                parent_map[child] = (
                    parent if parent in allowed else None
                )

            visit(child, visited)

    visited = set()

    for collection in scene.collection.children:
        visit(collection, visited)

    return parent_map


# ============================================================
# LOCATORS AND STORED TRANSFORMS
# ============================================================

def locator_name(collection):
    return f"{LOCATOR_PREFIX}{collection.name}"


def get_locator_collection(scene):
    return get_or_create_collection(
        scene.collection,
        LOCATOR_COLLECTION_NAME,
    )


def get_or_create_locator(collection, locator_collection):
    """
    Each source collection gets one locator empty.

    If the empty exists, its transform is authoritative.
    If it was deleted, recreate it from stored collection props.
    """

    name = locator_name(collection)
    locator = bpy.data.objects.get(name)

    if locator is not None and locator.get(LOCATOR_KEY) != collection.name:
        locator = None

    if locator is None:
        locator = bpy.data.objects.new(name, None)
        locator.empty_display_type = 'PLAIN_AXES'
        locator.empty_display_size = 0.5
        locator[LOCATOR_KEY] = collection.name

        locator_collection.objects.link(locator)

        # Restore stored transform when available.
        location = collection.get(PROP_LOCATION, (0, 0, 0))
        rotation = collection.get(
            PROP_ROTATION, (1, 0, 0, 0)
        )
        scale = collection.get(PROP_SCALE, (1, 1, 1))

        locator.location = location
        locator.rotation_mode = 'QUATERNION'
        locator.rotation_quaternion = Quaternion(rotation)
        locator.scale = scale

    else:
        # Ensure the locator is linked to the locator collection.
        if locator.name not in locator_collection.objects:
            locator_collection.objects.link(locator)

    return locator


def store_locator_transform(collection, locator):
    """Persist locator world transform on the source collection."""

    matrix = locator.matrix_world.copy()
    location, rotation, scale = matrix.decompose()

    collection[PROP_LOCATION] = tuple(location)
    collection[PROP_ROTATION] = tuple(rotation)
    collection[PROP_SCALE] = tuple(scale)


def get_stored_locator_matrix(collection):
    location = collection.get(PROP_LOCATION, (0, 0, 0))
    rotation = collection.get(
        PROP_ROTATION, (1, 0, 0, 0)
    )
    scale = collection.get(PROP_SCALE, (1, 1, 1))

    return (
        Matrix.Translation(location)
        @ Quaternion(rotation).to_matrix().to_4x4()
        @ Matrix.Diagonal((*scale, 1.0))
    )


# ============================================================
# WORLD-ALIGNED ASSETS
# ============================================================

def create_world_aligned_asset(
    source_collection,
    locator,
    world_scene,
):
    """
    Build an independent asset collection.

    Each direct member object is copied into the asset. Its transform
    becomes locator_world^-1 @ original_object_world, so the locator
    transform is removed from the asset and can be restored by a rig
    control.

    Object data and modifiers are retained; mesh geometry itself is
    not destructively modified.
    """

    asset = bpy.data.collections.new(
        f"{ASSET_PREFIX}{source_collection.name}"
    )
    asset[GENERATED_KEY] = True
    asset[SOURCE_KEY] = source_collection.name

    world_scene.collection.children.link(asset)

    inverse_locator = locator.matrix_world.inverted_safe()

    for source_obj in source_collection.objects:
        # Skip the helper locator if it happens to be a direct member.
        if source_obj.get(LOCATOR_KEY):
            continue

        new_obj = source_obj.copy()

        # Shared object data keeps the result lightweight.
        # Object transforms are independent.
        new_obj.name = (
            f"{source_obj.name}__{source_collection.name}_WA"
        )
        new_obj.parent = None

        asset.objects.link(new_obj)

        # Preserve the evaluated world placement relative to the
        # collection's locator origin.
        new_obj.matrix_world = (
            inverse_locator @ source_obj.matrix_world
        )

        new_obj[GENERATED_KEY] = True
        new_obj[SOURCE_KEY] = source_collection.name

    return asset


# ============================================================
# RIG CONTROLS
# ============================================================

def create_rig_control(
    source_collection,
    asset_collection,
    rig_scene,
    controls_collection,
    locator_matrix,
):
    """
    Create an empty that instances one world-aligned asset.
    The empty's transform restores the locator's world transform.
    """

    control = bpy.data.objects.new(
        f"{CONTROL_PREFIX}{source_collection.name}",
        None,
    )

    controls_collection.objects.link(control)

    control.empty_display_type = 'PLAIN_AXES'
    control.empty_display_size = 0.75
    control.instance_type = 'COLLECTION'
    control.instance_collection = asset_collection

    control.matrix_world = locator_matrix
    control[GENERATED_KEY] = True
    control[SOURCE_KEY] = source_collection.name

    return control


def parent_controls(controls, parent_map, collections):
    """
    Rebuild the source collection hierarchy with control empties.
    Set matrix_world after parenting so original world transforms
    remain unchanged.
    """

    for collection in collections:
        parent_collection = parent_map.get(collection)

        if parent_collection is None:
            continue

        child_control = controls[collection]
        parent_control = controls.get(parent_collection)

        if parent_control is None:
            continue

        world_matrix = child_control.matrix_world.copy()
        child_control.parent = parent_control
        child_control.matrix_world = world_matrix


# ============================================================
# MAIN BUILD
# ============================================================

def build_collection_pipeline():
    source_scene = bpy.context.scene

    if source_scene.name in (WORLD_SCENE_NAME, RIG_SCENE_NAME):
        raise RuntimeError(
            "Run this from the source scene, not a generated scene."
        )

    # Collect source data before deleting generated output.
    collections = get_source_collections(source_scene)

    if not collections:
        raise RuntimeError(
            "No source collections found below the active scene."
        )

    parent_map = get_collection_parent_map(
        source_scene,
        collections,
    )

    # Ensure every source collection has a locator.
    locator_collection = get_locator_collection(source_scene)
    locators = {}

    for collection in collections:
        locator = get_or_create_locator(
            collection,
            locator_collection,
        )
        locators[collection] = locator

    # Update dependencies so world transforms are current.
    bpy.context.view_layer.update()

    # Store locator transforms on the source collections.
    for collection, locator in locators.items():
        store_locator_transform(collection, locator)

    # Capture matrices before removing generated scenes.
    locator_matrices = {
        collection: locator.matrix_world.copy()
        for collection, locator in locators.items()
    }

    # Remove previous outputs and regenerate.
    remove_generated_scenes_and_data()

    world_scene = create_scene(WORLD_SCENE_NAME)
    rig_scene = create_scene(RIG_SCENE_NAME)

    world_scene[GENERATED_KEY] = True
    rig_scene[GENERATED_KEY] = True

    # Generate one aligned collection per source collection.
    assets = {}

    for collection in collections:
        assets[collection] = create_world_aligned_asset(
            collection,
            locators[collection],
            world_scene,
        )

    # Create a dedicated control collection in the rig scene.
    controls_collection = bpy.data.collections.new(
        "Rig_Controls"
    )
    controls_collection[GENERATED_KEY] = True
    rig_scene.collection.children.link(controls_collection)

    controls = {}

    for collection in collections:
        controls[collection] = create_rig_control(
            collection,
            assets[collection],
            rig_scene,
            controls_collection,
            locator_matrices[collection],
        )

    # Reconstruct the collection hierarchy.
    parent_controls(
        controls,
        parent_map,
        collections,
    )

    # Save source scene name for traceability.
    world_scene["_source_scene"] = source_scene.name
    rig_scene["_source_scene"] = source_scene.name

    print("Collection pipeline generated successfully.")
    print(f"Source: {source_scene.name}")
    print(f"World-aligned scene: {world_scene.name}")
    print(f"Rig scene: {rig_scene.name}")
    print(f"Collections processed: {len(collections)}")

    return world_scene, rig_scene


# ============================================================
# RUN
# ============================================================

build_collection_pipeline()
