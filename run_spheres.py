import subprocess
from sphere_settings import g_blender_excutable_path

if __name__ == '__main__':
    command = [g_blender_excutable_path, '--background', '-noaudio', '--python', 'render_spheres.py']
    subprocess.run(command)