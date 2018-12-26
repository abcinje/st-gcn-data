import argparse
import os

parser = argparse.ArgumentParser(description='Make json files from movies')
parser.add_argument('openpose', type=str, help='openpose directory path')
parser.add_argument('input', type=str, help='input path')
path = parser.parse_args().input+'/'

def run_openpose(video_path, save=None, hand=False, show=True, norm=False, two_people=True):
    write_json = ''
    display = ''
    option_hand = ''
    keypoint_scale = None
    max_people = None
    if save != None:
        write_json = '--write_json %s'%(save)
    if hand:
        option_hand = '--hand'
    if not show:
        display = '--display 0 --render_pose 0'
    if norm:
        keypoint_scale = '--keypoint_scale 3'
    if two_people:
        max_people = '--number_people_max 2'

    openpose = './build/examples/openpose/openpose.bin '
    option = '--video %s %s %s %s %s %s'%(video_path, option_hand, write_json,
                                            display, keypoint_scale, max_people)
    os.system(openpose+option)

if path[0] != '/':
    path = os.getcwd()+'/'+path

os.chdir(parser.parse_args().openpose)

dirname = os.path.dirname(path)+'_skeleton/'
if not os.path.exists(dirname):
    os.mkdir(dirname)

for (root, dirs, files) in os.walk(path):
    for fname in files:
        run_openpose(os.path.join(root, fname), dirname+fname,
                        show=False, norm=False, two_people=False)
