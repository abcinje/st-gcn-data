import argparse
import os
import json

parser = argparse.ArgumentParser(description="Normalize the coordinates of each parts and discard all frames with an index greater than 300.")
parser.add_argument("input", type=str, help="input path")
parser.add_argument("width", type=int, help="video width")
parser.add_argument("height", type=int, help="video height")

path = parser.parse_args().input+"/"
width = parser.parse_args().width
height = parser.parse_args().height

for (root, dirs, files) in os.walk(path):
    for fname in files:

        [name, ext] = os.path.splitext(fname)
        if ext != '.json':
            continue

        with open(os.path.join(root, fname), 'r') as f:
            data = json.load(f)

        new_data = {}
        new_data["data"] = data["data"][:299]
        new_data["label"] = data["label"]
        new_data["label_index"] = data["label_index"]

        for i in new_data["data"]:
            for j in i["skeleton"]:
                for k in range(len(j["pose"])):
                    if k%2 == 0:
                        j["pose"][k] = round(j["pose"][k]/float(width), 3)
                    else:
                        j["pose"][k] = round(j["pose"][k]/float(height), 3)

        with open(os.path.join(root, fname), 'w') as f:
            json.dump(new_data, f, sort_keys=True)

