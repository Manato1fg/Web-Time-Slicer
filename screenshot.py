import os
import sys
import argparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess

def escape_url(url):
    url = url.replace('&', '^&')
    return url

# ref. https://qiita.com/derodero24/items/17f24ed59d4f5650b3f5
def screenshot_full(driver, filename, timeout=30):
    '''take a full size screenshot'''
    url = driver.current_url
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")
    cmd = '"C:\Program Files\Google\Chrome\Application\chrome.exe"' \
        + ' --headless=new' \
        + ' --hide-scrollbars' \
        + ' --incognito' \
        + ' --disable-gpu' \
        + ' --screenshot="' + filename + '"'\
        + ' --window-size=' + str(w) + ',' + str(h) \
        + ' ' + f"{escape_url(url)}"
    # execute command
    subprocess.Popen(cmd, shell=True,
                     stdout=sys.stdout,
                     stderr=sys.stderr)

if __name__ == '__main__':
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image'), exist_ok=True)
    parser = argparse.ArgumentParser(description='script allows you to capture screenshots of specified URLs.')
    parser.add_argument('-u', '--url', help='url to take a screenshot', required=True)
    parser.add_argument('-o', '--output', help='output file name. if suffix is not specified, ".png" is added.', default='screen.png')
    parser.add_argument('-t', '--timeout', help='timeout (sec)', default=30)
    args = parser.parse_args()
    url = args.url
    output = args.output
    timeout = args.timeout
    if not output.endswith('.png'):
        output += '.png'
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"image{os.sep}{output}")
    driver = webdriver.Chrome()
    driver.get(url)
    screenshot_full(driver, filename)
    driver.quit()
    
    