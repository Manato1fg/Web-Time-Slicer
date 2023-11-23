# Twitter only accepts video files encoded with H.264(AAC) at 40fps or less.
# ref. https://gist.github.com/Manato1fg/dfbb83fa20125cef6f5cb1613a9bc499
import sys
import os
import subprocess
import argparse

def convert(inputfile: str):
    outputfile = inputfile.replace(".mp4", ".twitter.mp4")

    subprocess.call(
        ["ffmpeg", "-y", "-i", inputfile, "-vcodec", "libx264", "-acodec", "aac",  "-r", "30", "-ac", "2", outputfile],
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
if __name__ == "__main__":
    if not os.path.isdir("video"):
        print("video folder not found.")
        exit()
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--force', help='force conversion', action='store_true', default=False)
    args = args.parse_args()
    subfolders = [f.path for f in os.scandir("video") if f.is_dir()]
    for subfolder in subfolders:
        files = [f.path for f in os.scandir(subfolder) if f.is_file()]
        for file in files:
            if not file.endswith(".mp4"):
                continue
            if file.endswith(".twitter.mp4"):
                continue
            # already converted and not force
            if os.path.exists(file.replace(".mp4", ".twitter.mp4")) and not args.force:
                continue
            print(f"converting {file}...")
            convert(file)