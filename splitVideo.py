# import os
# import subprocess as sp


# #from http://stackoverflow.com/questions/22731999/python-video-editing-how-to-trim-videos

# def get_ffmpeg_bin():
# 	return "/usr/local/bin/ffmpeg"
#     # ffmpeg_dir = helper_functions.get_ffmpeg_dir_path()
#     # FFMPEG_BIN = os.path.join(ffmpeg_dir, "ffmpeg.exe")
#     # return FFMPEG_BIN


# def split_vid_from_path(video_file_path, start_time, end_time):
#     ffmpeg_binary =  get_ffmpeg_bin()
#     output_file_name = os.path.join("~/Documents/Scope", "00008_1.avi")
#     pipe = sp.Popen([ffmpeg_binary,"-v", "quiet", "-y", "-i", video_file_path, "-vcodec", "copy", "-acodec", "copy",
#                  "-ss", start_time, "-t", end_time, "-sn", output_file_name ])


#     pipe.wait()
#     return True


# sample_vid = os.path.join("~/Documents/Scope", "00008.avi")
# split_vid_from_path(sample_vid, "00:00:00", "00:00:17")

from moviepy.editor import *

video = VideoFileClip("00008.avi").subclip(50,60)
result = CompositeVideoClip([video])
result.write_videofile("00008_edited.mp4",fps=25)