g_shapenet_path = "/cluster/home/denysr/scratch/dataset/ShapeNetv2/ShapeNetCore.v2.zip"
# g_shapenet_path = "/cluster/home/denysr/scratch/dataset/sphere.zip"
g_texture_path = "/cluster/home/denysr/scratch/dataset/ShapeNetv2/textures.zip"
g_blender_path = r"/cluster/scratch/denysr/src/blender-2.91.0-linux64/blender"

import os 
if not os.path.exists(g_shapenet_path):
	g_shapenet_path = "/home/denysr/data/ShapeNetCore.v2.zip"
	g_texture_path = "/home/denysr/data/textures.zip"
	g_blender_path = r"/home/denysr/Programs/blender-2.91.0-linux64/blender"

# ensure that blender python has pillow pachage, e.g.
# /cluster/scratch/denysr/src/blender-2.91.0-linux64/2.91/python/bin/python3.7m -m pip install --target="/cluster/home/denysr/scratch/src/blender-2.91.0-linux64/2.91/python/lib/python3.7/"  pillow
