import os
import sys
import json
import zipfile
import numpy as np
from datetime import datetime

# enable importing from current dir when running with Blender
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from settings import *

from blender import render
from blender import utils

# restart with Blender if necessary
args = render.ensure_blender(g_blender_path)

n_sequences = int(args[0]) if len(args) else 5
out_dir = args[1] if len(args) > 1 else "."
do_shapenet = int(args[2]) if len(args) > 2 else 1

if do_shapenet:
    obj_path = g_shapenet_path
else:
    obj_path = g_spheres_path
print(obj_path)

objs = utils.ZipLoader(obj_path, "*.obj", balance_subdirs=True)
texs = utils.ZipLoader(g_texture_path, "*/textures_train/*.jpg")

p = dict(
    resolution=(320, 240),
    n_frames=24,
    blurs=[(0, 10), (-11, -1)],
    z_range=(-8, -3),
    delta_z=1,
    delta_xy=(0.5, 3),
    max_rot=np.pi / 8,
    render_backside=True,
)


render.init(p["n_frames"], p["resolution"])
frustum = render.Frustum(p["z_range"], p["resolution"])

time = datetime.now()
filename = time.strftime(f"fmo_{len(p['blurs'])}_{p['n_frames']}_%y%m%d%H%M%S.zip")

with zipfile.ZipFile(os.path.join(out_dir, filename), "w") as zip:
    zip.comment = json.dumps(p).encode()
    for i in range(n_sequences):
        print(f"Rendering {i} / {n_sequences} sequence.")
        obj = objs.get_random()
        tex = texs.get_random()
        loc = frustum.gen_point_pair(p["delta_z"], p["delta_xy"])
        rot_start = np.random.rand(3) * 2 * np.pi
        rot_end = rot_start + p["max_rot"] * (np.random.rand(3) * 2 - 1)
        name = f"{i:04}.webp"
        with objs.as_tempfile(obj) as objf, texs.as_tempfile(tex) as texf:
            with zip.open(name, "w") as out:
                render.render(out, objf, texf, loc, (rot_start, rot_end), p["blurs"],p["render_backside"])
        zip.getinfo(name).comment = json.dumps({"obj": obj, "tex": tex}).encode()

duration = datetime.now() - time
print(
    f"Rendered {n_sequences} sequences in {duration}, "
    f"{duration.total_seconds() / n_sequences:.2f}s per sequence"
)