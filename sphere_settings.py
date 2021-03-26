# bsub -W 120:00 -G ls_polle -n 4 -R "rusage[mem=10000, scratch=50000]" python3 run_spheres.py

import os

dataset_folder = '/mnt/lascar/rozumden/dataset/'
tmp_folder = '/home.stud/rozumden/tmp/'
g_blender_excutable_path = '/home.stud/rozumden/src/blender-2.79b-linux-glibc219-x86_64/blender'

if not os.path.exists(dataset_folder):
    dataset_folder = '/cluster/scratch/denysr/dataset/'
    tmp_folder = '/cluster/home/denysr/tmp/'
    g_blender_excutable_path = '/cluster/apps/blender/2.79b/x86_64/blender'


g_view_point_file = {'view_points/chair.txt', 'view_points/bottle.txt', 'view_points/diningtable.txt', 'view_points/sofa.txt', 'view_points/bed.txt'}

g_sphere_path = dataset_folder + '386.obj'

g_number_frames = 3

if True:
    print('Rendering training dataset')
    g_number = 1000
    g_texture_path = dataset_folder+'ShapeNetv2/textures/textures_train/' 
    g_background_image_path = dataset_folder+'vot/'
else:
    print('Rendering testing dataset')
    g_number = 20
    g_texture_path = dataset_folder+'ShapeNetv2/textures/textures_test/'
    g_background_image_path = dataset_folder+'vot/'
    # g_background_image_path = dataset_folder+'sports1m/seq/'

g_max_trials = 50 ## max trials per sample to generate a nice FMO (inside image, etc)

#folders to store synthetic data
# g_syn_rgb_folder = dataset_folder+'BlurredSpheres'+str(g_number)+'/' 
g_syn_rgb_folder = dataset_folder+'BlurredSpheres3Frames'+str(g_number)+'.hdf5' 
g_temp = g_syn_rgb_folder+"sphere_0001"+'/'

#camera:
#enum in [‘QUATERNION’, ‘XYZ’, ‘XZY’, ‘YXZ’, ‘YZX’, ‘ZXY’, ‘ZYX’, ‘AXIS_ANGLE’]
g_rotation_mode = 'XYZ'

#output:
g_fmo_steps = 24

#enum in [‘BW’, ‘RGB’, ‘RGBA’], default ‘BW’
g_rgb_color_mode = 'RGBA'
#enum in [‘8’, ‘10’, ‘12’, ‘16’, ‘32’], default ‘8’
g_rgb_color_depth = '16'
g_rgb_color_max = 255 #   2**int(g_rgb_color_depth)
g_rgb_file_format = 'PNG'

g_depth_use_overwrite = True
g_depth_use_file_extension = True
g_use_film_transparent = True

#dimension:

#engine type [CYCLES, BLENDER_RENDER]
g_engine_type = 'CYCLES'

#output image size =  (g_resolution_x * resolution_percentage%, g_resolution_y * resolution_percentage%)
g_resolution_x = 640
g_resolution_y = 480
g_resolution_percentage = 100/2
g_render_light = False
g_ambient_light = True
g_apply_texture = True
g_skip_low_contrast = True
g_skip_small = True
g_bg_color = (0.6, 0.6, 0.6) # (1.0,1.0,1.0) # (0.5, .1, 0.6)

#performance:

g_gpu_render_enable = False

#if you are using gpu render, recommand to set hilbert spiral to 256 or 512
#default value for cpu render is fine
g_hilbert_spiral = 512 

