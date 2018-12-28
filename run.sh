#!/bin/bash

if [[ $# != 4 ]]; then
    echo "Usage: ./run.sh <openpose directory> <input directory> <video width> <video height>"
    exit 0
fi

# Running OpenPose
python openpose.py $1 $2
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

# Merging json files
python merge.py $2_skeleton
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

# Normalization
python norm.py $2_skeleton_merged $3 $4
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

# Generating a summary file
python label_gen.py $2_skeleton_merged
