import bpy

# Set the name of the Image Plane object
object_name = "emissive_plane"

# Get a reference to the Image Plane object
obj = bpy.data.objects.get(object_name)

# Check if the object was found
if obj is not None:
    # Get a reference to the object's material
    material = obj.active_material

    # Get a reference to the material's image texture node
    image_node = material.node_tree.nodes.get("Image Texture")

    # Set the path to the new image file
    image_path = "/home/udit/Pictures/blender_test/MNIST/train-images-idx3-ubyte_train_folder/00002.png"

    # Load the new image file into Blender
    new_image = bpy.data.images.load(image_path)

    # Set the image node's image property to the new image
    image_node.image = new_image

    # Update the Image Plane's viewport display to show the new image
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.object.mode_set(mode="OBJECT")

    print("Image Plane updated with new image:", image_path)
else:
    print("Image Plane not found with name:", object_name)
