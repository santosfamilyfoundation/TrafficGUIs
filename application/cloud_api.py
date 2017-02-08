###This will hold all api calls for TrafficCloud
import os
import pickle
import uuid
import requests
from app_config import AppConfig as ac
import json

from pprint import pprint

class CloudWizard:
    def __init__(self, ip_addr, port=8088):
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
            with open('.IDdict','rb') as dict_file:
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

    def uploadVideo(self,  video_path, identifier = None):
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

    def uploadHomography(self,
                            aerial_path,\
                            camera_path,\
                            identifier,\
                            up_ratio,\
                            aerial_pts,\
                            camera_pts):
        files = {
            'aerial': open(aerial_path, 'rb'),
            'camera': open(camera_path, 'rb'),
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
                    max_features_per_frame = None,\
                    num_displacement_frames = None,\
                    min_feature_displacement = None,\
                    max_iterations_to_persist = None,\
                    min_feature_frames = None,\
                    max_connection_distance = None,\
                    max_segmentation_distance = None):

        print "configFiles called with identifier = {}"\
                .format(identifier)

        payload = {
            'identifier': identifier,
            'max_features_per_frame': max_features_per_frame,
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

    def analysis(self, identifier, email=None):
        print "analysis called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'analysis', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def objectTracking(self, identifier, email=None):
        print "objectTracking called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'objectTracking', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def safetyAnalysis(self, identifier, email=None):
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
        local_filename = 'highlight_video.mp4'
        r = requests.get(self.server_addr + 'retrieveResults', data = payload, stream=True)
        with open(local_filename, 'wb') as f:
            print('Dumping "{0}"...'.format(local_filename))
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        print "Status Code: {}".format(r.status_code)

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
