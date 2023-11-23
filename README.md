# Web Time Slicer

## Project Description
This Python application offers a novel approach to visualizing web content by turning website scrolling into a four-dimensional experience. It conceptualizes a two-dimensional website in a three-dimensional space composed of the x, y, and time (t) axes. The app creates dynamic, slit-scan style videos by 'slicing' through this space.
It supports <b>only</b> Windows right now.

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

`python slitscan.py [-w WIDTH] [-a ASPECT] [-f FPS] [-l LENGTH]`


### `convert_video.py`
Converts videos in the 'video' folder to a Twitter-compatible format (H.264 AAC at 40fps or less) and saves them as new files with a '.twitter.mp4' extension.

`python convert_video.py [-f]`

## LICENSE
MIT