import os

dataset_folder = '/mnt/lascar/rozumden/dataset/'
tmp_folder = '/home.stud/rozumden/tmp/'
g_blender_excutable_path = '/home.stud/rozumden/src/blender-2.79b-linux-glibc219-x86_64/blender'

if not os.path.exists(dataset_folder):
    dataset_folder = '/cluster/scratch/denysr/dataset/'
    tmp_folder = '/cluster/home/denysr/tmp/'
    # g_blender_excutable_path = 'blender'
    g_blender_excutable_path = '/cluster/apps/blender/2.79b/x86_64/blender'
    # MAKE SURE to have libraries: /cluster/apps/blender/2.79b/x86_64/2.79/python/bin/python3.5m -m pip install --user pillow


g_shapenet_path = dataset_folder+'ShapeNetv2/ShapeNetCore.v2'

g_view_point_file = {'view_points/chair.txt', 'view_points/bottle.txt', 'view_points/diningtable.txt', 'view_points/sofa.txt', 'view_points/bed.txt'}

g_render_objs_val = ['bottle', 'bowl', 'can', 'jar', 'mug']
# g_render_objs = ['table','jar', 'skateboard', 'car','bottle' , 'tower' ,'chair' ,'bookshelf' ,'camera' , 'airplane' ,'laptop' ,'basket' , 'sofa' ,'knife' , 'can' , 'rifle' , 'train' ,  'pillow' ,  'lamp' ,  'trash bin' , 'mailbox' , 'watercraft' , 'motorbike' , 'dishwasher' ,  'bench' , 'pistol' , 'rocket' , 'loudspeaker' , 'file cabinet' ,  'bag' , 'cabinet' , 'bed' , 'birdhouse' , 'display' , 'piano' , 'earphone' , 'telephone' , 'stove' , 'microphone','bus', 'mug', 'remote', 'bathtub' ,  'bowl' , 'keyboard', 'guitar' , 'washer', 'mobile phone' , 'faucet' , 'printer' , 'cap' , 'clock', 'helmet', 'flowerpot', 'microwaves']
g_render_objs_train = ['motorbike']
# g_render_objs_train = ['table','jar', 'skateboard', 'bottle' , 'tower' ,'chair' ,'bookshelf' ,'camera' ,'laptop' ,'basket' , 'sofa' ,'knife' , 'can' , 'rifle' , 'train' ,  'lamp' ,  'trash bin' , 'mailbox' , 'watercraft' , 'motorbike' , 'dishwasher' ,  'bench' , 'pistol' , 'rocket' , 'loudspeaker' , 'file cabinet' ,  'bag' , 'cabinet' , 'bed' , 'birdhouse' , 'display' , 'piano' , 'earphone' , 'telephone' , 'stove' , 'microphone', 'mug', 'remote', 'bathtub' ,  'bowl' , 'keyboard', 'guitar' , 'washer', 'faucet' , 'printer' , 'cap' , 'clock', 'helmet', 'flowerpot', 'microwaves']
g_render_objs = g_render_objs_train
# g_render_objs = list(set(g_render_objs_train) - set(g_render_objs_val))
# g_render_objs = ['mug','rifle','motorbike','dishwasher','pillow']

if True:
    print('Rendering training dataset')
    g_number_per_category = 1000
    g_texture_path = dataset_folder+'ShapeNetv2/textures/textures_train/' 
    g_background_image_path = dataset_folder+'vot/'
else:
    print('Rendering testing dataset')
    g_number_per_category = 20
    g_texture_path = dataset_folder+'ShapeNetv2/textures/textures_test/'
    g_background_image_path = dataset_folder+'sports1m/seq/'

g_max_trials = 50 ## max trials per sample to generate a nice FMO (inside image, etc)

#folders to store synthetic data
# g_syn_rgb_folder = dataset_folder+'ShapeNetv2/ShapeBlur'+str(g_number_per_category)+'/' 
g_syn_rgb_folder = dataset_folder+'ShapeNetv2/ShapeBlur'+str(g_number_per_category)+'.hdf5' 
# g_temp =           '/mnt/lascar/rozumden/dataset/ShapeNetv2/ShapeBlur/'
g_temp = g_syn_rgb_folder+g_render_objs[0]+'/'

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

#total 55 categories
g_shapenet_categlory_pair = {
    'table' : '04379243',
    'jar' : '03593526',
    'skateboard' : '04225987',
    'car' : '02958343',
    'bottle' : '02876657',
    'tower' : '04460130',
    'chair' : '03001627',
    'bookshelf' : '02871439',
    'camera' : '02942699',
    'airplane' : '02691156',
    'laptop' : '03642806',
    'basket' : '02801938',
    'sofa' : '04256520',
    'knife' : '03624134',
    'can' : '02946921',
    'rifle' : '04090263',
    'train' : '04468005',
    'pillow' : '03938244',
    'lamp' : '03636649',
    'trash bin' : '02747177',
    'mailbox' : '03710193',
    'watercraft' : '04530566',
    'motorbike' : '03790512',
    'dishwasher' : '03207941',
    'bench' : '02828884',
    'pistol' : '03948459',
    'rocket' : '04099429',
    'loudspeaker' : '03691459',
    'file cabinet' : '03337140',
    'bag' : '02773838',
    'cabinet' : '02933112',
    'bed' : '02818832',
    'birdhouse' : '02843684',
    'display' : '03211117',
    'piano' : '03928116',
    'earphone' : '03261776',
    'telephone' : '04401088',
    'stove' : '04330267',
    'microphone' : '03759954',
    'bus' : '02924116',
    'mug' : '03797390',
    'remote' : '04074963',
    'bathtub' : '02808440',
    'bowl' : '02880940',
    'keyboard' : '03085013',
    'guitar' : '03467517',
    'washer' : '04554684',
    'mobile phone' : '02992529', #
    'faucet' : '03325088',
    'printer' : '04004475',
    'cap' : '02954340',
    'clock' : '03046257',
    'helmet' : '03513137',
    'flowerpot' : '03991062',
    'microwaves' : '03761084'
}

# bicycle 02834778