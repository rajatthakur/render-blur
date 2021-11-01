import os
import sys
import json
import zipfile
import numpy as np
from datetime import datetime
import csv
import pdb

# enable importing from current dir when running with Blender
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from settings import *

from blender import render
from blender import utils

# restart with Blender if necessary
args = render.ensure_blender(g_blender_path)

n_sequences = int(args[0]) if len(args) else 5
out_dir = args[1] if len(args) > 1 else "."
# obj_path = str(args[2]) if len(args) > 2 else g_objects_path
# tex_path = str(args[3]) if len(args) > 3 else g_texture_path

obj_path = g_objects_path
tex_path = g_texture_path

objs = utils.ZipLoader(obj_path, "*.obj", balance_subdirs=True)
texs = utils.ZipLoader(tex_path, "*/textures_train/*.jpg")

render_params = dict(
    resolution=(320, 240),
    n_frames=24,
    blurs=[(0, 10), (-11, -1)],
    z_range=(-6, -3),
    delta_z=1,
    delta_xy=(0.3, 1.5),
    max_rot=np.pi / 6,
    render_backside=True,
)

render.init(render_params["n_frames"], render_params["resolution"], 40, (0.6, 0.6, 0.6))
frustum = render.Frustum(render_params["z_range"], render_params["resolution"])

time = datetime.now()
filename = time.strftime(f"output/fmo_{len(render_params['blurs'])}_{render_params['n_frames']}_%y%m%d%H%M%S.zip")
filename_csv = time.strftime(f"output/fmo_{len(render_params['blurs'])}_{render_params['n_frames']}_%y%m%d%H%M%S.csv")

with zipfile.ZipFile(os.path.join(out_dir, filename), "w") as zip:
    zip.comment = json.dumps(render_params).encode()
    with open(os.path.join(out_dir, filename_csv), "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Object', 'Texture', 'Output', 'Rotation_Start', 'Rotation_End'])
        for i in range(n_sequences):
            print(f"Rendering {i} / {n_sequences} sequence.")
            obj = objs.get_random()
            tex = texs.get_random()
            loc = frustum.gen_point_pair(render_params["delta_z"], render_params["delta_xy"])
            rot_start = np.random.rand(3) * 2 * np.pi
            rot_end = rot_start + render_params["max_rot"] * (np.random.rand(3) * 2 - 1)
            name = f"{i:04}.webp"
            with objs.as_tempfile(obj) as objf, texs.as_tempfile(tex) as texf:
                with zip.open(name, "w") as out:
                    render.render(out, objf, texf, loc, (rot_start, rot_end), render_params["blurs"],
                                  render_params["render_backside"])
            zip.getinfo(name).comment = json.dumps({"obj": obj, "tex": tex}).encode()
            csv_writer.writerow([obj, tex, name, rot_start, rot_end])


duration = datetime.now() - time
print(
    f"Rendered {n_sequences} sequences in {duration}, "
    f"{duration.total_seconds() / n_sequences:.2f}s per sequence"
)
