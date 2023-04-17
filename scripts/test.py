import bpy
import mathutils
import math

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

# Create a plane with size 20cm x 20cm at the origin and make it green
scattering_wall = bpy.ops.mesh.primitive_plane_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 0))
scattering_wall_obj = bpy.context.active_object
scattering_wall_obj.name = "scattering_wall"
scattering_wall_mat = bpy.data.materials.new(name="ScatteringMat")
scattering_wall_mat.diffuse_color = (0, 1, 0)
scattering_wall_obj.data.materials.append(scattering_wall_mat)


# Create occluder wall size 50cm x 50cm perpendicular to the above wall at a distance of 20cm from the center of the wall
occluder_wall = bpy.ops.mesh.primitive_plane_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 0.35))
occluder_wall_obj = bpy.context.active_object
occluder_wall_obj.name = "occluder_wall"
occluder_wall_obj.rotation_euler = mathutils.Euler((math.radians(90), 0, 0), 'XYZ')

# Create a point light on the right-hand side of "occluder_wall"
light_data = bpy.data.lights.new(name="Light", type='POINT')
light = bpy.data.objects.new(name="Light", object_data=light_data)
bpy.context.scene.collection.objects.link(light)
light.data.color = (0, 1, 0) # Set the light color to white
light.location = (0.0, 0.25, 0.25)

# Create a new cube object
bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, location=(0, 0.0, 0.0))
# Set the material for the cube
material = bpy.data.materials.new(name="Cube Material")
material.diffuse_color = (0.8, 0.2, 0.2)  # Red
bpy.context.active_object.data.materials.append(material)

# Create a 720p camera and set its location and rotation and other properties
camera_data = bpy.data.cameras.new(name='Camera')
camera = bpy.data.objects.new(name='camera', object_data=camera_data)
bpy.context.scene.collection.objects.link(camera)

bpy.context.scene.camera = bpy.data.objects['Camera']
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

# Set resolution and aspect ratio
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.pixel_aspect_x = 1
bpy.context.scene.render.pixel_aspect_y = 1
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.film_transparent = False
bpy.context.scene.world.horizon_color = (0.2, 0.2, 0.2) 
bpy.context.scene.render.image_settings.color_mode = 'RGB'

bpy.context.scene.camera = bpy.data.objects['Camera']

output_path = "/home/udit/Pictures/blender_test"
file_name = "output.jpg"
# Set up the render settings
# Render the image
bpy.ops.render.render(write_still=True)
file_path = f'{output_path}/{file_name}'
# Save the rendered image to disk
bpy.data.images['Render Result'].save_render(filepath=file_path)
print(f"File save at {file_path}")