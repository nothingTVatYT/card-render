import bpy
from math import *
from mathutils import *
import random
import glob
import re

def next_output_name():
    idx=0
    for file in glob.glob('result-*.*'):
        regex_match=re.match("result-(\d+)", file)
        if regex_match:
            idx=max(idx,int(regex_match.groups()[0]))
    idx+=1
    return f"result-{idx}.jpg"

def look_at(camera, point):
    #loc_camera = camera.matrix_world.to_translation()
    loc_camera = camera.location
    direction = point - loc_camera
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

# -------------------------------------------------------------
# parameters you can change to create varying results
# -------------------------------------------------------------
# textures to use
#card_texture='texture/nyid.jpg'
#card_texture='texture/MargaretFishing_01_1.png'
card_texture='texture/target-gift-card-back.jpg'
#tabletop_color='texture/Wood049_2K_Color.jpg'
#tabletop_displacement='texture/Wood049_2K_Displacement.jpg'
#tabletop_normal='texture/Wood049_2K_Normal.jpg'
#tabletop_roughness='texture/Wood049_2K_Roughness.jpg'
tabletop_color='texture/Marble007_2K_Color.jpg'
tabletop_displacement='texture/Marble007_2K_Displacement.jpg'
tabletop_normal='texture/Marble007_2K_Normal.jpg'
tabletop_roughness='texture/Marble007_2K_Roughness.jpg'
# environmental lighting
hdri='texture/HDRI/lebombo_2k.hdr'
# random table rotation angle in degrees
rnd_tabletop=45
# random card location in meters
rnd_card_location=0.05
# random card rotation angle in degrees
rnd_card=20
# camera location relative to the card
#  cam_x is forward/backward, cam_y is left/right, cam_z is up/down
cam_x=-0.09
cam_y=0
cam_z=0.27
# set to True for out-of-focus shots
out_of_focus=False
# focus plane distance (only if out_of_focus=True)
focus_distance=10
# -------------------------------------------------------------

# get object pointers
card = bpy.data.objects['Card']
tabletop = bpy.data.objects['Tabletop']
cam = bpy.data.objects['Camera']

# randomize tabletop rotation
tabletop.rotation_euler[2]+=(random.random()-0.5)*rnd_tabletop/180*pi

# randomize card position
card.location[0]+=(random.random()-0.5)*rnd_card_location
card.rotation_euler[2]+=(random.random()-0.5)*rnd_card/180*pi

# position the camera (forward/backward, left/right, up/down)
#print(f"current cam location: {cam.location-card.location}")
cam.location=card.location+Vector((cam_x,cam_y,cam_z))

# make sure the camera is pointing to the card
# before you use world coordinates: bpy.context.view_layer.update()
#look_at(cam, card.matrix_world.to_translation())
look_at(cam, card.location)

# set the textures (only update file paths)
bpy.data.images['nyid.jpg'].filepath=card_texture
bpy.data.images['Wood049_2K_Color.jpg'].filepath=tabletop_color
bpy.data.images['Wood049_2K_Displacement.jpg'].filepath=tabletop_displacement
bpy.data.images['Wood049_2K_Normal.jpg'].filepath=tabletop_normal
bpy.data.images['Wood049_2K_Roughness.jpg'].filepath=tabletop_roughness
bpy.data.images['lebombo_2k.hdr'].filepath=hdri

if out_of_focus:
	bpy.data.cameras["Camera"].dof.focus_object=None
	bpy.data.cameras["Camera"].dof.focus_distance=focus_distance

# render the scene
file = next_output_name()
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.filepath = file
bpy.ops.render.render(write_still=True)
