# Data Preprocessing Tools for ST-GCN

## Prerequisites
- Python3
- [OpenPose](https://github.com/yysijie/openpose)
- FFmpeg

## Setting FPS to 30 (optional)
```
python fps.py <input directory>
```

## Normalization
```
python norm.py <input directory> <video width> <video height>
```

## Generating a summary file
```
python label_gen.py <input directory>
```
