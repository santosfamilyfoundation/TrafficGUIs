
import cv2
import os

def convert_video_to_frames(video_path, images_dir, prefix='image-', extension='png'):
	if not os.path.exists(video_path):
		return False

	if not os.path.exists(images_dir):
		os.makedirs(images_dir)

	vidcap = cv2.VideoCapture(video_path)
	count = 0
	success = True
	while success:
		success, image = vidcap.read()
		if success:
			if '.' in extension:
				format_string = "%d"
			else:
				format_string = "%d."
			filename = prefix + format_string + extension
			cv2.imwrite(os.path.join(images_dir, filename % count), image)     # save frame as JPEG file
			count += 1


