###This will hold all api calls for TrafficCloud
import os
import pickle
import uuid
import requests
from app_config import AppConfig as ac

from pprint import pprint

def CloudWizard(ip_addr,*arg):
        return TrafficCloud(ip_addr)
class TrafficCloud:
    def __init__(self,ip_addr):
        #TODO: Needs to be done in sync with server
        #   not a uuid creation
        #self._ids = self.readIds()
        #self.project_path = project_path
        #self._ids[self.project_path] = uuid.uuid4()
        #self._writeIds()
        if ip_addr == 'localhost':
            self.server_ip = '127.0.0.1'
        else:
            self.server_ip = ip_addr

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

    def uploadVideo(self, identifier=None):

        print "uploadVideo called with identifier = {}".format(identifier)
        with open(ac.CURRENT_PROJECT_VIDEO_PATH, 'rb') as video:
            payload = {
                'video.%s'%video_extn : video,
                'identifier': identifier
            }
            r = requests.post("http://"+self.server_ip + '/uploadVideo', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)
        #TO-DO: Add returned identifier to internal storage


    def uploadHomography(self, identifier):

        print "uploadHomography called with identifier = {}".format(identifier)
        homography_path = os.path.join(ac.CURRENT_PROJECT_PATH, "homography")

        with open(os.path.join(homography_path, "aerial.png"), 'rb') as hg_aerial,\
             open(os.path.join(homography_path, "camera.png"), 'rb') as hg_camera,\
             open(os.path.join(homography_path, "homography.txt"), 'rb') as hg_txt:

            files = {
                'homography/aerial.png': hg_aerial,
                'homography/camera.png': hg_camera,
                'homography/homography.txt': hg_txt
            }
            r = requests.post("http://" + self.server_ip + '/uploadHomography',files = files)

        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)


    def uploadFiles(self):

        print "uploadFiles called"
        project_name = ac.CURRENT_PROJECT_PATH.strip('/').split('/')[-1]
        homography_path = os.path.join(ac.CURRENT_PROJECT_PATH, "homography")

        video_extn = ac.CURRENT_PROJECT_VIDEO_PATH.split('.')[-1]

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
                ".temp/test/test_feature/feature_tracking.cfg": test_track,
                'video.%s'%video_extn : video
            }
            r = requests.post("http://" + self.server_ip + '/upload',files = files)
            print r.text;

###############################################################################
# Configuration Functions
###############################################################################

    def configFiles(self, identifier, filename, config_data):
        print "testConfig called with identifier = {} and filename = {}"\
                .format(identifier,filename)

        print "config_data is as follows:"
        pprint(config_data)

        payload = {
            'identifier': identifier,
            'filename': filename
        }

        r = requests.post("http://"+self.server_ip + '/config', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def testConfig(self, test_flag, identifier, frame_start = 0, num_frames = 100):
        print "testConfig called with identifier = {}, test_flag = {}, frame_start = {}, and num_frames = {}"\
                .format(identifier,test_flag,frame_start,num_frames)

        payload = {
            'test_flag': test_flag,
            'identifier': identifier,
            'frame_start': frame_start,
            'num_frames': num_frames
        }

        r = requests.post("http://"+self.server_ip + '/testConfig', data = payload)
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

        r = requests.post("http://"+self.server_ip + '/analysis', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def objectTracking(self, identifier, email):
        print "objectTracking called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post("http://"+self.server_ip + '/objectTracking', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def safetyAnalysis(self, identifier, email):
        print "safetyAnalysis called with identifier = {} and email = {}".format(identifier, email)

        payload = {
            'identifier': identifier,
            'email': email
        }

        r = requests.post("http://"+self.server_ip + '/safetyAnalysis', data = payload)
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
        }

        if not (ttc_threshold == None):
            payload['ttc_threshold'] = ttc_threshold
        if not (vehicle_only == None):
            payload['vehicle_only'] = vehicle_only

        r = requests.post("http://"+self.server_ip + '/highlightVideo', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def makeReport(self, identifier):
        print "makeReport called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }

        r = requests.post("http://"+self.server_ip + '/makeReport', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def retrieveResults(self, identifier):
        print "retrieveResults called with identifier = {}".format(identifier)

        payload = {
            'identifier': identifier,
        }

        r = requests.get("http://"+self.server_ip + '/retrieveResults', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

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

        r = requests.post("http://"+self.server_ip + '/roadUserCounts', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)

    def speedCDF(self, identifier, ttc_threshold = None, vehicle_only = None):
        print "speedCDF called with identifier = {}, ttc_threshold = {} and vehicle_only = {}"\
                .format(identifier, ttc_threshold, vehicle_only)

        payload = {
            'identifier': identifier,
        }

        if not (ttc_threshold == None):
            payload['ttc_threshold'] = ttc_threshold
        if not (vehicle_only == None):
            payload['vehicle_only'] = vehicle_only

        r = requests.post("http://"+self.server_ip + '/speedCDF', data = payload)
        print "Status Code: {}".format(r.status_code)
        print "Response Text: {}".format(r.text)


#FOR TESTING PURPOSES ONLY
if __name__ == '__main__':
    print "Syntax looks fine!"
    #remote = CloudWizard('10.7.90.25')
    #local = CloudWizard('localhost')
    #server = TrafficCloud_Server("/project/path/goes/ahere","localhost")
    #print remote.server_ip
    #print remote.readIds()
    #print local.server_ip
    #print local.readIds()