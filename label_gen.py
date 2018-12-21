import argparse
import os
import json

parser = argparse.ArgumentParser(description="Generate a summary file of the json data.")
parser.add_argument("input", type=str, help="input path")
path = parser.parse_args().input+"/"

summary = {}

for (root, dirs, files) in os.walk(path):
    for fname in files:

        [name, ext] = os.path.splitext(fname)
        if ext != '.json':
            continue

        with open(os.path.join(root, fname)) as f:
            data = json.load(f)

            has_skeleton = (data["data"] != [])
            entry = {"has_skeleton": has_skeleton, "label": data["label"], "label_index": data["label_index"]}
            summary[name] = entry

output_path = os.path.dirname(path)+"_label.json"
with open(output_path, 'w') as output:
    json.dump(summary, output, indent=4, sort_keys=True)

