import bpy
import mathutils
import math


def delete_everythin_in_the_scene():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects in the scene and delete them
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Remove all materials from the material slots
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    # Remove all textures from the texture slots
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

    # Remove all images from the image slots
    for image in bpy.data.images:
        bpy.data.images.remove(image)

def save_rendered_image(output_path = "/home/udit/Pictures/blender_test", file_name = "output.jpg"):
    output_path = "/home/udit/Pictures/blender_test"
    file_name = "output.jpg"
    # Set up the render settings
    bpy.context.scene.render.resolution_x = 640
    bpy.context.scene.render.resolution_y = 480
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.engine = 'CYCLES'
    # Render the image
    bpy.ops.render.render(write_still=True)
    file_path = f'{output_path}/{file_name}'
    # Save the rendered image to disk
    bpy.data.images['Render Result'].save_render(filepath=file_path)
    print(f"File save at {file_path}")


# Create a plane with size 20cm x 20cm at the origin and make it green
scattering_wall = bpy.ops.mesh.primitive_plane_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 0))
scattering_wall_obj = bpy.context.active_object
scattering_wall_obj.name = "scattering_wall"
scattering_wall_mat = bpy.data.materials.new(name="ScatteringMat")
scattering_wall_mat.diffuse_color = (0, 1, 0)
scattering_wall_obj.data.materials.append(scattering_wall_mat)

# Create occluder wall size 50cm x 50cm perpendicular to the above wall at a distance of 20cm from the center of the wall
occluder_wall = bpy.ops.mesh.primitive_plane_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 0.3))
occluder_wall_obj = bpy.context.active_object
occluder_wall_obj.name = "occluder_wall"
occluder_wall_obj.rotation_euler = mathutils.Euler((math.radians(90), 0, 0), 'XYZ')

# Create a point light on the right-hand side of "Wall2"
light_data = bpy.data.lights.new(name="Light", type='POINT')
light = bpy.data.objects.new(name="Light", object_data=light_data)
bpy.context.scene.collection.objects.link(light)
light.data.color = (1, 1, 1) # Set the light color to white
light.location = (0.0, 0.25, 0.25)

# Create a 720p camera and set its location and rotation and other properties
camera_data = bpy.data.cameras.new(name='Camera')
camera = bpy.data.objects.new(name='camera', object_data=camera_data)
bpy.context.scene.collection.objects.link(camera)

# Set camera properties
camera.data.type = 'PERSP'
camera.data.lens = 35
camera.data.clip_start = 0.1
camera.data.clip_end = 1000
camera.data.sensor_width = 32
camera.data.sensor_height = 18
camera.data.sensor_fit = 'HORIZONTAL'
camera.data.angle = math.radians(45) # 45 degrees in radians
camera.location = (0.0, -0.25, 0.25)
camera.rotation_euler = mathutils.Euler((0, math.radians(-30), math.radians(90)), 'XYZ')

# Set up the render settings
# Set resolution and aspect ratio
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.pixel_aspect_x = 1
bpy.context.scene.render.pixel_aspect_y = 1
bpy.context.scene.render.engine = 'CYCLES'

output_path = "/home/udit/Pictures/blender_test"
file_name = "scattering_1080.png"
# Render the image
bpy.ops.render.render(write_still=True)
file_path = f'{output_path}/{file_name}'
# Save the rendered image to disk
bpy.data.images['Render Result'].save_render(filepath=file_path)
print(f"File save at {file_path}")
