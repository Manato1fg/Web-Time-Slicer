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

## Showcase
### T
  
https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/7ee0ac5a-6ed8-4723-8d6d-b0800e5b984a

### X

https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/2c64cb64-01fe-4a93-b471-d05b3377585f

### Y
 
https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/67e2f50b-5a50-42f7-bbbe-9f4b121a5111

### Yaw

https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/84b77890-2bdb-488e-bb87-22b63516573e

### Pitch

https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/c9f0a849-47d1-4a96-8d65-06500dc9fbf3

### Roll

https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/f0d9dbbb-9ac1-4de8-bdcf-ba91b6c3b4c8

### Time Wave

https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/f22d1229-891f-4f1c-9d38-e04829d99d39

### Sin 

https://github.com/Manato1fg/Web-Time-Slicer/assets/21980635/78ac853e-9284-4fe8-b00b-a2bd4734188b

