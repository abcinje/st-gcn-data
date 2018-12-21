import argparse
import os

parser = argparse.ArgumentParser(description="Set FPS of each movie to 30.")
parser.add_argument("input", type=str, help="input path")
path = parser.parse_args().input+"/"

dirname = os.path.dirname(path)+"_30fps/"
if not os.path.exists(dirname):
    os.mkdir(dirname)    

for (root, dirs, files) in os.walk(path):
    for fname in files:
        # TODO : Time Intervals
        os.system("ffmpeg -i %s -ss %d -t %d -vf minterpolate=fps=30 -q 0 %s" %(os.path.join(root, fname), 0, 10, dirname+fname))

