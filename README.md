# Web Time Slicer

## Project Description
This Python application offers a novel approach to visualizing web content by turning website scrolling into a four-dimensional experience. It conceptualizes a two-dimensional website in a three-dimensional space composed of the x, y, and time (t) axes. The app creates dynamic, slit-scan style videos by 'slicing' through this space.
It supports <b>only</b> Windows right now.

## Example


https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/e784e47f-318c-4163-bb30-63989f54e78b



https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/4e85bfc8-fdc8-4243-92a1-75f863ef27b2



https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/3e67c3db-df18-46c6-aab0-98b9c5bb95b1



## Installation Instructions
To set up this application, follow these steps:
1. **Install Required Packages**: Install the necessary Python packages listed in the `requirements.txt` file using the command:

    `pip install -r requirements.txt`

2. **Install ffmpeg for Video Uploads**: If you plan to upload videos to Twitter, ensure that ffmpeg is installed on your system. For installation instructions, visit the [ffmpeg official website](https://ffmpeg.org/download.html).

## Usage

### `screenshot.py`
Captures screenshots of specified URLs. The screenshots are saved in the 'image' folder.

`python screenshot.py -u [URL] [-o OUTPUT] [-t TIMEOUT]`


### `slitscan.py`
Processes images from the 'image' folder, creating slit-scan videos. These videos are saved in corresponding folders within the 'video' folder.

`slitscan.py [-h] [-w WIDTH] [-a ASPECT] [-f FPS] [-l LENGTH] [-fi FILTER] [--fast]`

- `-fi`: if no filter name is given, it applies all available filters.  
- `--fast` mode demands high memory usage.

Example:<br />
```Shell
python slitscan.py -w 800 -a 4/3 -f 60 -fi pitch --fast
```


### `convert_video.py`
Converts videos in the 'video' folder to a Twitter-compatible format (H.264 AAC at 40fps or less) and saves them as new files with a '.twitter.mp4' extension.

`python convert_video.py [-f]`

## LICENSE
MIT
