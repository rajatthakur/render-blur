g_shapenet_path = "/cluster/home/denysr/scratch/dataset/ShapeNetv2/ShapeNetCore.v2.zip"
g_spheres_path = "resources/sphere.zip"
g_texture_path = "resources/textures.zip"
g_blender_path = r"/Applications/Blender.app/Contents/MacOS/Blender"

import os 
if not os.path.exists(g_shapenet_path):
	g_shapenet_path = "/home/denysr/data/ShapeNetCore.v2.zip"
	g_spheres_path = "resources/sphere.zip"
	g_texture_path = "resources/textures.zip"
	g_blender_path = r"/Applications/Blender.app/Contents/MacOS/Blender"

if not os.path.exists(g_shapenet_path):
	g_shapenet_path = "/home/rozumden/data/ShapeNetCore.v2.zip"
	g_spheres_path = "resources/sphere.zip"
	g_texture_path = "resources/textures.zip"
	g_blender_path = r"/Applications/Blender.app/Contents/MacOS/Blender"

# ensure that blender python has pillow pachage, e.g.
# /cluster/scratch/denysr/src/blender-2.91.0-linux64/2.91/python/bin/python3.7m -m pip install --target="/cluster/home/denysr/scratch/src/blender-2.91.0-linux64/2.91/python/lib/python3.7/"  pillow
