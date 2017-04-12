
import json
import os
import subprocess
try:
	from PIL import Image
except:
	import Image

def save_video_frame(video_path, image_path):
    if os.path.exists(video_path):
        cmd = "ffmpeg -y -i %s -t 1 -vframes 1 -f image2 %s" % (video_path, image_path)
        subprocess.check_call(cmd, shell=True)

def get_video_resolution(videopath):
    """
    Returns
    -------
    (width, height) in number of pixels
    """
    out = subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', videopath])
    out = json.loads(out)
    return (out['streams'][0]['width'], out['streams'][0]['height'])
