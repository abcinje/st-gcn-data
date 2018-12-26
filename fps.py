import argparse
import os

parser = argparse.ArgumentParser(description="Set FPS of each movie to 30.")
parser.add_argument("input", type=str, help="input path")
parser.add_argument("-s", "--start", type=int, default=0, help="start time")
path = parser.parse_args().input+"/"

def run_ffmpeg(input_path, output_path, start_time=0):
    os.system("ffmpeg -i %s -ss %d -t %d -vf minterpolate=fps=30 -q 0 %s"
                %(input_path, start_time, start_time+10, output_path))

dirname = os.path.dirname(path)+"_30fps/"
if not os.path.exists(dirname):
    os.mkdir(dirname)    

for (root, dirs, files) in os.walk(path):
    for fname in files:
        run_ffmpeg(os.path.join(root, fname), dirname+fname, parser.parse_args().start)
