###This will hold all api calls for TrafficCloud
import os
import pickle
import uuid
import requests
from requests_toolbelt import MultipartEncoder
from app_config import AppConfig as ac
from app_config import get_project_path
import json
from threading import Timer
import numpy as np

from pprint import pprint

class CloudWizard:
    def __init__(self, ip_addr, port=8088):
        self.set_url(ip_addr, port=port)

    def set_url(self, ip_addr, port=8088):
        protocol = self.protocol_from_url_string(ip_addr)
        if protocol == None:
            protocol = 'http://'

        (addr, p) = self.ip_and_port_from_url_string(ip_addr)
        if addr == 'localhost':
            addr = '127.0.0.1'

        # Use port specified by string, otherwise fall back to default port
        if p == None:
            p = port

        self.server_addr = protocol + addr + ':{}/'.format(port)

###############################################################################
# Upload Functions
###############################################################################

    def uploadVideo(self,  video_path):
        print "uploadVideo called"
        with open(video_path, 'rb') as video:
            # We set the content-disposition 'filename' parameter manually
            # incase we need to do streaming
            files = {'video' : (os.path.basename(video_path), video)}

            #Use a multipartencoder to stream the file data as just data
            m = MultipartEncoder(fields = files)

            # m.len returns the size of all of the encoded parts in bytes
            # and 1024*1024 is MB in bytes. As such we can compare the size
            # of all the files we want to send to a 100MB size limit for
            # transitioning to streaming rather than loading into memory
            if m.len/(1024*1024) >= 100:
                # We need to set the Content-Type header
                r = requests.post(\
                    self.server_addr + 'uploadVideo', data = m,\
                    headers = {'Content-Type': m.content_type})
            else:
                r = requests.post(\
                    self.server_addr + 'uploadVideo', files = files)

        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)
        print "Response JSON: {}".format(r.json())
        return r.json()['identifier']

    def uploadMask(self, identifier, mask_path):
        print "uploadMask called"
        with open(mask_path, 'rb') as mask:
            extn = os.path.basename(mask_path).split('.')[-1]
            files = {'mask.%s' % extn :  mask}
            payload = {'identifier': identifier}
            r = requests.post(self.server_addr + 'mask', data = payload, files = files)

        print "Status Code: {}".format(r.status_code)

###############################################################################
# Configuration Functions
###############################################################################

    def configHomography(self,
                            identifier,\
                            up_ratio,\
                            aerial_pts,\
                            camera_pts):
        payload = {
            'identifier': identifier,
            'unit_pixel_ratio': up_ratio,
            'aerial_pts': json.dumps(aerial_pts),
            'camera_pts': json.dumps(camera_pts)
        }

        r = requests.post(\
            self.server_addr + 'homography', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def getHomography(self, identifier, file_path = None):
        payload = {'identifier': identifier}
        r = requests.get(\
            self.server_addr + 'homography', params = payload)

        print "Response JSON: {}".format(r.json())
        print "Status Code: {}".format(r.status_code)
        homography = r.json()['homography']
        if file_path:
            path = os.path.join(file_path, 'homography.txt')
            np.savetxt(path, np.array(homography))
        return homography

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

    def testConfig(self, identifier, test_flag,
                   frame_start = None,\
                   num_frames = None):
        print "testConfig called with identifier = {},\
                test_flag = {}, frame_start = {}, and num_frames = {}"\
                .format(identifier,test_flag,frame_start,num_frames)

        status_dict = self.getProjectStatus(identifier)
        if status_dict["homography"] != 2:
            print "Check your homography and upload (again)."
            return

        payload = {
            'test_flag': test_flag,
            'identifier': identifier,
            'frame_start': frame_start,
            'num_frames': num_frames
        }

        r = requests.post(self.server_addr + 'testConfig', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def getTestConfig(self, identifier, test_flag, file_path):
        print "getTestConfig called with identifier = {} and test_flag = {}".format(identifier,test_flag)

        payload = {
            'test_flag': test_flag,
            'identifier': identifier
        }

        if test_flag == 'feature':
            path = os.path.join(file_path, 'feature_video.mp4')
        elif test_flag == 'object':
            path = os.path.join(file_path, 'object_video.mp4')
        else:
            print "ERROR: Invalid flag"
            return

        r = requests.get(self.server_addr + 'testConfig', params = payload, stream=True)

        with open(path, 'wb') as f:
            print('Dumping "{0}"...'.format(path))
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        print "Status Code: {}".format(r.status_code)

    def defaultConfig(self):
        r = requests.get(self.server_addr + 'defaultConfig')
        return r.json()

###############################################################################
# Analysis Functions
###############################################################################

    def analysis(self, identifier, email=None):
        print "analysis called with identifier = {} and email = {}".format(identifier, email)

        status_dict = self.getProjectStatus(identifier)
        if status_dict["homography"] != 2:
            print "Check your homography and upload (again)."
            return

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'analysis', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def objectTracking(self, identifier, email=None):
        print "objectTracking called with identifier = {} and email = {}".format(identifier, email)

        status_dict = self.getProjectStatus(identifier)
        if status_dict["homography"] != 2:
            print "Check your homography and upload (again)."
            return

        payload = {
            'identifier': identifier,
            'email': email
        }
        r = requests.post(self.server_addr + 'objectTracking', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def safetyAnalysis(self, identifier, email=None):
        print "safetyAnalysis called with identifier = {} and email = {}".format(identifier, email)

        status_dict = self.getProjectStatus(identifier)
        if status_dict["homography"] != 2:
            print "Check your homography and upload (again)."
            return
        elif status_dict["object_tracking"] != 2:
            print "Check object tracking and run (again)."
            return

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post(self.server_addr + 'safetyAnalysis', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

###############################################################################
# Status Checking Functions
###############################################################################

    def getProjectStatus(self, identifier):

        payload = {
            'identifier': identifier,
        }

        r = requests.get(self.server_addr + 'status', params = payload)
        status_dict = r.json()
        status_dict = {k:int(v) for (k,v) in status_dict.iteritems()}
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)
        return status_dict

###############################################################################
# Results Functions
###############################################################################

    def results(self, identifier, ttc_threshold = None, vehicle_only = None, speed_limit = None):
        print "results called with identifier = {}, ttc_threshold = {}, vehicle_only = {}, and speed_limit= {}"\
                .format(identifier, ttc_threshold, vehicle_only, speed_limit)

        # sync calls
        self.roadUserCounts(identifier)
        self.speedDistribution(identifier, speed_limit, vehicle_only)

        self.makeReport(identifier)

        # async calls
        self.highlightVideo(identifier, ttc_threshold, vehicle_only)

    def highlightVideo(self, identifier, ttc_threshold = None, vehicle_only = None):
        print "highlightVideo called with identifier = {}, ttc_threshold = {} and vehicle_only = {}"\
                .format(identifier, ttc_threshold, vehicle_only)

        status_dict = self.getProjectStatus(identifier)
        if status_dict["homography"] != 2:
            print "Check your homography and upload (again)."
            return
        elif status_dict["object_tracking"] != 2:
            print "Check object tracking and run (again)."
            return
        elif status_dict["safety_analysis"] != 2:
            print "Check safety analysis and run (again)."
            return

        payload = {
            'identifier': identifier,
            'ttc_threshold': ttc_threshold,
            'vehicle_only': vehicle_only
        }

        r = requests.get(self.server_addr + 'highlightVideo', params = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def makeReport(self, identifier, file_path):
        print "makeReport called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }

        r = requests.get(self.server_addr + 'makeReport', params  = payload)
        path = os.path.join(file_path, 'santosreport.pdf')
        if os.path.exists(path):
            os.remove(path)

        with open(path, 'wb') as f:
            print('Dumping "{0}"...'.format(path))
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        print "Status Code: {}".format(r.status_code)

    def retrieveResults(self, identifier, file_path):
        print "retrieveResults called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }
        path = os.path.join(file_path, 'results.zip')
        if os.path.exists(path):
            os.remove(path)
        r = requests.get(self.server_addr + 'retrieveResults', params = payload, stream=True)
        with open(path, 'wb') as f:
            print('Dumping "{0}"...'.format(path))
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        print "Status Code: {}".format(r.status_code)

    def roadUserCounts(self, identifier, file_path):
        print "roadUserCounts called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }

        r = requests.get(self.server_addr + 'roadUserCounts', params = payload, stream=True)
        path = os.path.join(file_path, 'road_user_icon_counts.jpg')
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'wb') as f:
            print('Dumping "{0}"...'.format(path))
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        print "Status Code: {}".format(r.status_code)

    def speedDistribution(self, identifier, file_path, speed_limit = None, vehicle_only = None):
        print "speedDistribution called with identifier = {}, speed_limit = {} and vehicle_only = {}"\
                .format(identifier, speed_limit, vehicle_only)

        payload = {
            'identifier': identifier,
            'speed_limit': speed_limit,
            'vehicle_only': vehicle_only
        }

        r = requests.get(self.server_addr + 'speedDistribution', params = payload, stream=True)
        path = os.path.join(file_path, 'velocityPDF.jpg')
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'wb') as f:
            print('Dumping "{0}"...'.format(path))
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        print "Status Code: {}".format(r.status_code)

###############################################################################
# Helper Methods
###############################################################################

    @classmethod
    def ip_and_port_from_url_string(cls, url):
        # Strip protocol if exists
        protocol = cls.protocol_from_url_string(url)
        if protocol:
            url = url[len(protocol):]

        # Now we should only have IP:PORT
        if ':' in url:
            l = url.split(':')
            return (l[0], l[1])
        else:
            return (url, None)

    @classmethod
    def protocol_from_url_string(cls, url):
        protocols = ['http://', 'https://']
        for protocol in protocols:
            if url.startswith(protocol):
                return protocol
        return None

# Define singleton to be used everywhere
api = CloudWizard('localhost')

###############################################################################
# Poll for Status with Callback
###############################################################################

class StatusPoller(object):
    def __init__(self, identifier, status_name, interval, callback):
        self._timer = None
        self.identifier = identifier
        self.status_name = status_name
        self.interval = interval
        self.callback = callback
        self.is_running = False
        self.has_run = False

    def _run(self):
        self.is_running = False
        self.start()

        self._poll_for_status()

    def _poll_for_status(self):
        status_dict = api.getProjectStatus(self.identifier)

        if self.status_name not in status_dict.keys():
            print(self.status_name + ' not in status dictionary')
        elif status_dict[self.status_name] == 2:
            self.stop()
            self.callback()
        elif status_dict[self.status_name] == 1:
            print(self.status_name + ' is still running')
        else:
            print(self.status_name + ' is not running, not continuing to poll for status')
            self.stop()

    def start(self):
        if not self.is_running:
            # If it's the first time, run it immediately
            if not self.has_run:
                self._timer = Timer(0, self._run)
                self.has_run = True
            else:
                self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

