
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

def get_video_resolution(video_path):
    """Gets video resolution in (width, height)"""
    if os.path.exists(video_path):
    	temp_image_path = os.path.join(os.path.dirname(video_path), 'temp.png')
    	save_video_frame(video_path, temp_image_path)
    	im = Image.open(temp_image_path)
    	size = im.size
    	os.remove(temp_image_path)
    	return size

