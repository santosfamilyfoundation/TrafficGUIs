
import cv2
import os

def convert_video_to_frames(video_path, images_dir, prefix, image_extension):
	if not os.path.exists(video_path):
		return False

	if not os.path.exists(images_dir):
		os.makedirs(images_dir)

	vidcap = cv2.VideoCapture(video_path)
	success,image = vidcap.read()
	count = 0
	success = True
	while success:
		success, image = vidcap.read()
		print 'Read a new frame: ', success
		if success:
			if '.' in image_extension:
				format_string = "%d"
			else:
				format_string = "%d."
			filename = prefix + format_string + image_extension
			cv2.imwrite(filename % count, image)     # save frame as JPEG file
			count += 1


