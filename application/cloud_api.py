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

    def testFeatureAnalysis(self, config, frames, callback):
        raise NotImplementedError("testFeatureAnalysis not yet implemented")

    def testObjectAnalysis(self, config, frames, callback):
        raise NotImplementedError("testFeatureAnalysis not yet implemented")

    def runTrajectoryAnalysis(self, config, callback):
        raise NotImplementedError("runTrajectoryAnalysis not yet implemented")

    def runSafetyAnalysis(self, prediction, db, callback):
        raise NotImplementedError("runSafetyAnalysis  not yet implemented")

    def runVisualization(self, db, callback):
        raise NotImplementedError("runVisualization not yet implemented")

    def getDB(self, callback):
        raise NotImplementedError("getDB not yet implemented")

    def getStatus(self, callback):
        raise NotImplementedError("getStatus not yet implemented")

    def generateDefaultConfig(self, callback):
        raise NotImplementedError("generateDefaultConfig not yet implemented")

#FOR TESTING PURPOSES ONLY
if __name__ == '__main__':
    remote = CloudWizard('10.7.90.25')
    local = CloudWizard('localhost')
    #server = TrafficCloud_Server("/project/path/goes/ahere","localhost")
    print remote.server_ip
    print remote.readIds()
    print local.server_ip
    print local.readIds()