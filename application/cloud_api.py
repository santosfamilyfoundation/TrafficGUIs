###This will hold all api calls for TrafficCloud
import os
import pickle
import uuid
import requests
from app_config import AppConfig as ac
import json

from pprint import pprint

def CloudWizard(ip_addr, port=8088):
    return TrafficCloud(ip_addr, port)

class TrafficCloud:
    def __init__(self, ip_addr, port):
        #TODO: Needs to be done in sync with server
        #   not a uuid creation
        #self._ids = self.readIds()
        #self.project_path = project_path
        #self._ids[self.project_path] = uuid.uuid4()
        #self._writeIds()
        if ip_addr == 'localhost':
            self.server_addr = 'http://127.0.0.1:{}/'.format(port)
        else:
            self.server_addr = 'http://{}:{}/'.format(ip_addr, port)

###############################################################################
# ID Storage Functions
###############################################################################

    def _initializeIds(self):
        with open('.IDdict','wb') as blank_dict_file:
                pickle.dump({},blank_dict_file)
        return {}

    def readIds(self):
        if os.path.isfile('.IDdict'):
            with open('.Iddict','rb') as dict_file:
                ids = pickle.loads(dict_file.read())
            return ids
        else:
            return self._initializeIds()

    def _writeIds(self):
        if os.path.isfile('.IDdict'):
            with open('.IDdict','wb') as dict_file:
                pickle.dump(self._ids,dict_file)
            return
        else:
            return self._initializeIds()

###############################################################################
# Upload Functions
###############################################################################

    def uploadVideo(self,  video_path, identifier = None,):
        print "uploadVideo called with identifier = {}".format(identifier)
        with open(video_path, 'rb') as video:
            files = {'video' : video}
            payload = {'identifier': identifier}
            r = requests.post(\
                self.server_addr + 'uploadVideo',\
                data = payload, files = files, stream = True)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)
        print "Response JSON: {}".format(r.json())
        return r.json()
        #TO-DO: Add returned identifier to internal storage

    def _local_uploadHomography(self, homography_path,\
                                identifier,\
                                up_ratio,\
                                aerial_pts,\
                                camera_pts):
        files = {
            'aerial': open(os.path.join(homography_path, "aerial.png"), 'rb'),
            'camera': open(os.path.join(homography_path, "camera.png"), 'rb'),
        }
        payload = {
            'identifier': identifier,
            'unit_pixel_ratio': up_ratio,
            'aerial_pts': json.dumps(aerial_pts),
            'camera_pts': json.dumps(camera_pts)
        }

        r = requests.post(\
            self.server_addr + 'uploadHomography',\
            data = payload, files = files)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def uploadHomography(self, identifier):
        print "uploadHomography called with identifier = {}".format(identifier)
        homography_path = os.path.join(ac.CURRENT_PROJECT_PATH, "homography")
        files = {
            'aerial': open(os.path.join(homography_path, "aerial.png"), 'rb'),
            'camera': open(os.path.join(homography_path, "camera.png"), 'rb'),
        }
        payload = {'identifier':identifier}
        r = requests.post(\
            self.server_addr + 'uploadHomography',\
            data = payload, files = files)

        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)


    def uploadFiles(self):
        print "uploadFiles called"
        project_name = ac.CURRENT_PROJECT_PATH.strip('/').split('/')[-1]
        homography_path = os.path.join(ac.CURRENT_PROJECT_PATH, "homography")

        video_extn = ac.CURRENT_PROJECT_VIDEO_PATH.split('.')[-1]
        print ac.CURRENT_PROJECT_VIDEO_PATH

        with open(os.path.join(homography_path, "aerial.png"), 'rb') as hg_aerial,\
             open(os.path.join(homography_path, "camera.png"), 'rb') as hg_camera,\
             open(os.path.join(homography_path, "homography.txt"), 'rb') as hg_txt,\
             open(os.path.join(ac.CURRENT_PROJECT_PATH, project_name  + ".cfg"), 'rb') as cfg_prname,\
             open(os.path.join(ac.CURRENT_PROJECT_PATH, "tracking.cfg"), 'rb') as cfg_track,\
             open(os.path.join(ac.CURRENT_PROJECT_PATH, ".temp/test/test_object/object_tracking.cfg"), 'rb') as test_obj,\
             open(os.path.join(ac.CURRENT_PROJECT_PATH, ".temp/test/test_feature/feature_tracking.cfg"), 'rb') as test_track,\
             open(ac.CURRENT_PROJECT_VIDEO_PATH, 'rb') as video:

            files = {
                'homography/aerial.png': hg_aerial,
                'homography/camera.png': hg_camera,
                'homography/homography.txt': hg_txt,
                'project_name.cfg': cfg_prname,
                'tracking.cfg': cfg_track,
                '.temp/test/test_object/object_tracking.cfg': test_obj,
                '.temp/test/test_feature/feature_tracking.cfg': test_track,
                'video.%s'%video_extn : video
            }
            r = requests.post(self.server_addr+'upload',files = files)
            print r.text;

###############################################################################
# Configuration Functions
###############################################################################

    def configFiles(self, identifier,
                    max_feature_per_frame = None,\
                    num_displacement_frames = None,\
                    min_feature_displacement = None,\
                    max_iterations_to_persist = None,\
                    min_feature_frames = None,\
                    max_connection_distance = None,\
                    max_segmentation_distance = None):

        print "testConfig called with identifier = {}"\
                .format(identifier,filename)

        payload = {
            'identifier': identifier,
            'max_feature_per_frame': max_feature_per_frame,
            'num_displacement_frames': num_displacement_frames,
            'min_feature_displacement': min_feature_displacement,
            'max_iterations_to_persist': max_iterations_to_persist,
            'min_feature_frames': min_feature_frames,
            'max_connection_distance': max_connection_distance,
            'max_segmentation_distance': max_segmentation_distance
        }
        print "config_data is as follows:"
        pprint(payload)

        r = requests.post(self.server_addr + 'config', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def testConfig(self, test_flag, identifier,
                   frame_start = None,\
                   num_frames = None):
        print "testConfig called with identifier = {},\
                test_flag = {}, frame_start = {}, and num_frames = {}"\
                .format(identifier,test_flag,frame_start,num_frames)

        payload = {
            'test_flag': test_flag,
            'identifier': identifier,
            'frame_start': frame_start,
            'num_frames': num_frames
        }

        r = requests.post(self.server_addr + 'testConfig', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)


###############################################################################
# Analysis Functions
###############################################################################

    def analysis(self, identifier, email):
        print "analysis called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'analysis', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def objectTracking(self, identifier, email):
        print "objectTracking called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'objectTracking', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def safetyAnalysis(self, identifier, email):
        print "safetyAnalysis called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'safetyAnalysis', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

###############################################################################
# Results Functions
###############################################################################

    def highlightVideo(self, identifier, ttc_threshold = None, vehicle_only = None):
        print "highlightVideo called with identifier = {}, ttc_threshold = {} and vehicle_only = {}"\
                .format(identifier, ttc_threshold, vehicle_only)

        payload = {
            'identifier': identifier,
            'ttc_threshold': ttc_threshold,
            'vehicle_only': vehicle_only
        }

        r = requests.post(self.server_addr + 'highlightVideo', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def makeReport(self, identifier):
        print "makeReport called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }

        r = requests.post(self.server_addr + 'makeReport', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def retrieveResults(self, identifier):
        print "retrieveResults called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }
        file_path = download_file(self.server_addr + 'retrieveResults', data = payload)
        print file_path
        #print "Status Code: {}".format(r.status_code)
        #print "Response Text: {}".format(r.text)

    #Helper Method for Downloading Files from URL
    def download_file(url):
        local_filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            print('Dumping "{0}"...'.format(local_filename))
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename

    def roadUserCounts(self, identifier):
        print "roadUserCounts called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }

        r = requests.post(self.server_addr + 'roadUserCounts', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def speedCDF(self, identifier, speed_limit = None, vehicle_only = None):
        print "speedCDF called with identifier = {}, speed_limit = {} and vehicle_only = {}"\
                .format(identifier, speed_limit, vehicle_only)

        payload = {
            'identifier': identifier,
            'speed_limit': speed_limit,
            'vehicle_only': vehicle_only
        }

        r = requests.post(self.server_addr + 'speedCDF', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)


#FOR TESTING PURPOSES ONLY
if __name__ == '__main__':
    print "Syntax looks fine!"

    ###########################################################################
    # Setup CloudWizard
    ###########################################################################
    #remote = CloudWizard('10.7.88.26')
    #remote = CloudWizard('10.26.89.15')
    remote = CloudWizard('10.7.24.20')

    ###########################################################################
    # Upload Video
    ###########################################################################
    video_path = '/home/user/Documents/output.mp4'
    #video_path = '/home/user/Documents/stmarc_video.avi'
    #video_path = '/home/user/Documents/Harvey_30min_day.mp4'
    id = remote.uploadVideo(video_path)['identifier']

    ###########################################################################
    # Upload Homography
    ###########################################################################
    print id
    aerial = [\
            (695.7036743164062, 406.8148193359375),\
            (819.7777709960938, 240.1481475830078),\
            (856.8148193359375, 553.111083984375),\
            (830.888916015625, 390.1481628417969),\
            (932.74072265625, 397.5555419921875)]
    camera = [\
            (614.2222290039062, 703.111083984375),\
            (936.4444580078125, 419.77777099609375),\
            (197.55555725097656, 630.888916015625),\
            (519.7777709960938, 330.8888854980469),\
            (558.6666870117188, 536.4444580078125)]
    remote._local_uploadHomography(\
            '/home/user/Documents/TrafficGUIs/project_dir/TestClassification/homography/',\
            id, 0.05, aerial, camera)

    ###########################################################################
    # Run Analysis Route
    ###########################################################################
    #remote.analysis(id,'phillip.seger@students.olin.edu')
    remote.objectTracking(id,'jacob.riedel@students.olin.edu')
    remote.safetyAnalysis(id,'jacob.riedel@students.olin.edu')




