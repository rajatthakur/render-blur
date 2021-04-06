import os
import sys
import random
import tempfile
from PIL import Image


def ensure_blender(blender=None):
    try:
        global bpy
        import bpy

        return sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    except ImportError:
        if blender:
            import subprocess

            print("Restarting with Blender...")
            sys.stdout.flush()
            sys.stderr.flush()
            subprocess.run([blender, "--background", "-noaudio", "--python", sys.argv[0], "--"] + sys.argv[1:])
            sys.exit()
        else:
            sys.exit("Failed to import bpy. Please run with Blender.")


def init(frames, resolution, mblur=40, env_light=(0.5, 0.5, 0.5)):
    ensure_blender()
    scene = bpy.context.scene

    # output settings
    scene.frame_start = scene.frame_current = 0
    scene.frame_end = frames - 1
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.film_transparent = True

    # canonical scene
    scene.camera.location = 0, 0, 0
    scene.camera.rotation_euler = 0, 0, 0
    scene.objects["Light"].location = 0, 0, 0
    scene.objects["Light"].data.energy = 0
    
    # environment lighting
    bpy.context.scene.world.use_nodes = False
    bpy.context.scene.world.color = env_light

    # remove default cube
    bpy.ops.object.delete()
    bpy.data.objects.remove(scene.objects["Light"])
    
    # create material for texture
    mat = bpy.data.materials.new("Texture")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    tex = nodes.new("ShaderNodeTexImage")
    mat.node_tree.links.new(tex.outputs[0], nodes["Principled BSDF"].inputs[0])

    # motion blur parameters
    scene.eevee.motion_blur_position = "START"
    scene.eevee.motion_blur_steps = mblur

def crop_image(orig_img, cropped_min_x, cropped_max_x, cropped_min_y, cropped_max_y):
    '''Crops an image object of type <class 'bpy.types.Image'>.  For example, for a 10x10 image, 
    if you put cropped_min_x = 2 and cropped_max_x = 6,
    you would get back a cropped image with width 4, and 
    pixels ranging from the 2 to 5 in the x-coordinate

    Note: here y increasing as you down the image.  So, 
    if cropped_min_x and cropped_min_y are both zero, 
    you'll get the top-left of the image (as in GIMP).

    Returns: An image of type  <class 'bpy.types.Image'>
    '''

    num_channels=orig_img.channels
    #calculate cropped image size
    cropped_size_x = cropped_max_x - cropped_min_x
    cropped_size_y = cropped_max_y - cropped_min_y
    #original image size
    orig_size_x = orig_img.size[0]
    orig_size_y = orig_img.size[1]

    cropped_img = bpy.data.images.new(name="cropped_img", width=cropped_size_x, height=cropped_size_y)

    print("Exctracting image fragment, this could take a while...")

    #loop through each row of the cropped image grabbing the appropriate pixels from original
    #the reason for the strange limits is because of the 
    #order that Blender puts pixels into a 1-D array.
    current_cropped_row = 0
    for yy in range(orig_size_y - cropped_max_y, orig_size_y - cropped_min_y):
        #the index we start at for copying this row of pixels from the original image
        orig_start_index = (cropped_min_x + yy*orig_size_x) * num_channels
        #and to know where to stop we add the amount of pixels we must copy
        orig_end_index = orig_start_index + (cropped_size_x * num_channels)
        #the index we start at for the cropped image
        cropped_start_index = (current_cropped_row * cropped_size_x) * num_channels 
        cropped_end_index = cropped_start_index + (cropped_size_x * num_channels)

        #copy over pixels 
        cropped_img.pixels[cropped_start_index : cropped_end_index] = orig_img.pixels[orig_start_index : orig_end_index]

        #move to the next row before restarting loop
        current_cropped_row += 1

    return cropped_img

def render(output, obj, tex, loc, rot, blurs=[(0, -1)], render_backside=False, crop_tex=True):
    ensure_blender()
    scene = bpy.context.scene

    # load object
    bpy.ops.import_scene.obj(filepath=obj)
    obj = bpy.context.selected_objects[0]

    # load texture
    if tex:
        tex = bpy.data.images.load(os.path.abspath(tex))
        if crop_tex:
            res = 32
            cx = random.randint(0,tex.size[0]-res-1)
            cy = random.randint(0,tex.size[1]-res-1)
            tex = crop_image(tex, cx, cx+res, cy, cy+res)
        mat = bpy.data.materials["Texture"]
        mat.node_tree.nodes["Image Texture"].image = tex
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.cube_project(scale_to_bounds=True)
        bpy.ops.object.editmode_toggle()

    # starting position
    obj.location = loc[0]
    obj.rotation_euler = rot[0]
    obj.keyframe_insert("location")
    obj.keyframe_insert("rotation_euler")

    # final position
    obj.location = loc[1]
    obj.rotation_euler = rot[1]
    obj.keyframe_insert("location", frame=scene.frame_end)
    obj.keyframe_insert("rotation_euler", frame=scene.frame_end)

    # linear movement
    for f in obj.animation_data.action.fcurves:
        for k in f.keyframe_points:
            k.interpolation = "LINEAR"

    # render to temp dir then pack to webp
    with tempfile.TemporaryDirectory() as tmp:

        # render frames
        scene.eevee.use_motion_blur = False
        scene.render.filepath = os.path.join(tmp, "frame")
        bpy.ops.render.render(animation=True)

        # render blurs
        scene.eevee.use_motion_blur = True
        for i, blur in enumerate(blurs):
            blur_start, blur_end = [b % (scene.frame_end + 1) for b in blur]
            scene.frame_current = blur_start
            scene.eevee.motion_blur_shutter = blur_end - blur_start
            scene.render.filepath = os.path.join(tmp, f"blur{i:04}")
            bpy.ops.render.render(write_still=True)
        scene.frame_current = scene.frame_start

        if render_backside:
            scene.eevee.use_motion_blur = False
            obj.rotation_euler = rot[0]
            obj.rotation_euler[0] += 3.1415926535897932384626433
            obj.keyframe_insert("rotation_euler")
            scene.render.filepath = os.path.join(tmp, "frame_rot")
            bpy.ops.render.render(write_still=True)

        # pack to webp
        fs = sorted([os.path.join(tmp, f) for f in os.listdir(tmp)])
        Image.open(fs[0]).save(
            output,
            format="webp",
            save_all=True,
            append_images=(Image.open(f) for f in fs[1:]),
            method=4,
            quality=75,
            duration=[1000] * len(blurs) + [33] * (scene.frame_end + 1 + int(render_backside)),
            minimize_size=True,
        )

    # clean up
    bpy.ops.object.delete()
    for collection in [bpy.data.meshes, bpy.data.materials, bpy.data.images]:
        for block in collection:
            if not block.users:
                collection.remove(block)


class Frustum:
    def __init__(
        self, z_range, resolution, max_radius=0.6, dead_zone=0.05, focal_length=50, sensor_size=36
    ):
        self.tan = (1 - dead_zone) * sensor_size / focal_length / 2
        self.offset = max_radius / self.tan * (self.tan ** 2 + 1) ** 0.5
        self.ratio = resolution[1] / resolution[0]
        self.z_range = z_range

    def gen_point(self, z=None):
        if z is None:
            z_min, z_max = self.z_range
            z = z_min + random.random() * (z_max - z_min)
        x = (random.random() * 2 - 1) * self.tan * (z + self.offset)
        y = (random.random() * 2 - 1) * self.tan * (z * self.ratio + self.offset)
        return x, y, z

    def gen_point_near(self, point, max_delta_z, delta_xy_range):
        x, y, z = point
        dxy_min, dxy_max = min(delta_xy_range) ** 2, max(delta_xy_range) ** 2
        for _ in range(100000):
            x2, y2, z2 = self.gen_point(z + max_delta_z * (random.random() * 2 - 1))
            if dxy_min <= (x - x2) ** 2 + (y - y2) ** 2 <= dxy_max:
                return x2, y2, z2
        raise ValueError("Failed to generate point in given range. Check input parameters.")

    def gen_point_pair(self, max_delta_z, delta_xy_range):
        for _ in range(50):
            a = self.gen_point()
            try:
                b = self.gen_point_near(a, max_delta_z, delta_xy_range)
            except ValueError:
                continue
            return a, b
        raise ValueError("Failed to generate point pair. Check input parameters.")
