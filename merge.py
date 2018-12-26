import argparse
import os
import json

from dict import label_rec
from dict import label_ntu

##
## make_data_dict(openpose_save, node=18, hand=False)
##   openpose_save (ex. '/home/user/example/')
##   node (18 or 25)
##   hand (Bool type)
##
## save_json(final_dict, json_path)
##   final_dict (output of make_data_dict)
##   json_path (ex. '/home/user/example.json')
##

def make_data_dict(openpose_save, node=18, hand=False):

    frame_index = 0
    data = []
    files = [i for i in os.listdir(openpose_save) if os.path.isfile(openpose_save+i)]
    files.sort()
    for fname in files:
        f = open(os.path.join(openpose_save, fname))
        json_data = json.load(f)
        people_list = json_data["people"]
        frame_index += 1
        if frame_index >= 300:
            continue
        data_dict = {"frame_index": frame_index}
        mean_score = []
        skel_list = []
        for i in range(len(people_list)):
            skel_dict = dict()
            a = []
            pose_list = []
            score_list = []
            a = people_list[i]["pose_keypoints_2d"]
            if node == 18:
                pose_list = [a[j] for j in range(57) if not (j+1)%3==0]
                pose_list[16:18] = []
            elif node == 25:
                pose_list = [a[j] for j in range(75) if not (j+1)%3==0]
            for x in range(len(pose_list)):
                if x%2 == 0:
                    pose_list[x] = round(pose_list[x]/1920, 3)
                else:
                    pose_list[x] = round(pose_list[x]/1080, 3)
            if node == 18:
                score_list = [round(a[j],3) for j in range(57) if (j+1)%3==0]
                del score_list[8]
            elif node == 25:
                score_list = [round(a[j],3) for j in range(75) if (j+1)%3==0]
            if hand:
                rhand = []
                lhand = []
                bhand = []
                hand_list = []
                hand_score = []
                rhand = people_list[i]["hand_right_keypoints_2d"][3:]
                lhand = people_list[i]["hand_left_keypoints_2d"][3:]
                bhand = rhand + lhand
                hand_list = [bhand[j] for j in range(120) if (j+1)%3!=0]
                for x in range(len(hand_list)):
                    if x%2 == 0:
                        hand_list[x] = round(hand_list[x]/1920, 3)
                    else:
                        hand_list[x] = round(hand_list[x]/1080, 3)
                pose_list = pose_list + hand_list
                hand_score = [round(bhand[j],3) for j in range(120) if (j+1)%3==0]
                score_list = score_list + hand_score
            skel_dict["pose"] = pose_list
            skel_dict["score"] = score_list
            n_of_node = len(score_list) - score_list.count(0)
            try:
                mean_score.append(sum(score_list)/n_of_node)
            except ZeroDivisionError:
                mean_score.append(0)
            skel_list.append(skel_dict)
        while len(mean_score) >= 3:
            k = []
            k = [x for x, y in enumerate(mean_score) if y==min(mean_score)]
            del skel_list[k[0]]
            del mean_score[k[0]]
        data_dict["skeleton"] = skel_list
        data.append(data_dict)
    final_dict = {"data": data}
    return final_dict

def save_json(final_dict, json_path):
    with open(json_path, 'w') as f:
        json.dump(final_dict, f)

parser = argparse.ArgumentParser(description='Merge json files from each movie into single json file.')
parser.add_argument('input', type=str, help='input path')
path = parser.parse_args().input + '/'

dirname = os.path.dirname(path) + '_merged/'
if not os.path.exists(dirname):
    os.mkdir(dirname)

openpose_file = os.listdir(path)
openpose_file.sort()

for fname in openpose_file:

    split = fname.split('A')
    ntu_index = int(split[1][1:3])
    if not ntu_index in label_ntu.keys():
        continue

    json_dir = path+fname+'/'
    data_dict = make_data_dict(json_dir, 18)
    label = label_ntu[ntu_index]
    label_index = label_rec[label]
    data_dict['label'] = label
    data_dict['label_index'] = label_index
    json_name = dirname + os.path.splitext(fname)[0] + '.json'
    save_json(data_dict, json_name)
    print(json_name + ' saved')
