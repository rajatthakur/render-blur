bsub -G ls_polle -W 24:00 -oo /cluster/home/denysr/tmp/lsf_tmp.txt -n 1 -R "rusage[mem=20000, scratch=50000]" python3 run_spheres.py
