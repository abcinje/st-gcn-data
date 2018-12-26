# Data Preprocessing Tools for ST-GCN

## Prerequisites
- Python3
- [OpenPose](https://github.com/yysijie/openpose)
- [FFmpeg](https://www.ffmpeg.org)

## Setting FPS to 30 (optional)
```
python fps.py [-s start_time] <input directory>
```

## Running OpenPose
```
python openpose.py <openpose directory> <input directory>
```

## Normalization
```
python norm.py <input directory> <video width> <video height>
```

## Generating a summary file
```
python label_gen.py <input directory>
```
