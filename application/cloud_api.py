###This will hold all api calls for TrafficCloud
import os
import requests
from requests_toolbelt import MultipartEncoder
from app_config import AppConfig as ac
from app_config import get_project_path
from threading import Timer
import numpy as np

from multiprocess import Process, Queue
from Queue import Empty as EmptyQueue
import time, signal

class CloudWizard:
    def __init__(self, ip_addr, port=8888):
        self.set_url(ip_addr, port=port)

    def set_url(self, ip_addr, port=8888):
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

    def parse_error(self, r):
        content_type = r.headers['content-type']
        if 'application/json' not in content_type:
            return (True, None, None)
        try:
            data = r.json()
        except ValueError:
            # If no JSON, also no error message
            return (True, None, None)
        if 'error' in data:
            return (False, data['error']['error_message'], data)
        else:
            return (True, None, data)

###############################################################################
# Helper Methods
###############################################################################

    def writeToPath(self,request, file_path,file_name):
        path = os.path.join(file_path, file_name)
        if os.path.exists(path):
            os.remove(path)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        with open(path, 'wb') as f:
            print('Dumping "{0}"...'.format(path))
            for chunk in request.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)

    def connectionError(self):
        message = 'Connection to server "{}" is offline'.format(self.server_addr)
        print(message)
        return (False, message, None)

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

###############################################################################
# Upload Functions
###############################################################################

    def uploadVideo(self, video_path):
        '''
            If success returns as false, the data field will contain the raw dictionary response from the server or None
        '''
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
            try:
                if m.len/(1024*1024) >= 100:
                    # We need to set the Content-Type header
                    r = requests.post(\
                        self.server_addr + 'uploadVideo', data = m,\
                        headers = {'Content-Type': m.content_type})
                else:
                    r = requests.post(\
                        self.server_addr + 'uploadVideo', files = files)
            except requests.exceptions.ConnectionError as e:
                return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            data = data['identifier']

        return (success, err, data)

    def uploadMask(self, identifier, mask_path):
        print "uploadMask called"
        with open(mask_path, 'rb') as mask:
            extn = os.path.basename(mask_path).split('.')[-1]
            files = {'mask.%s' % extn :  mask}
            payload = {'identifier': identifier}

            try:
                r = requests.post(self.server_addr + 'mask', json = payload, files = files)
            except requests.exceptions.ConnectionError as e:
                return self.connectionError()

            return self.parse_error(r)

        return (False, "Couldn't open mask file", None)

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
            'aerial_pts': aerial_pts,
            'camera_pts': camera_pts
        }

        try:
            r = requests.post(\
                self.server_addr + 'homography', json = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

    def getHomography(self, identifier, file_path = None):
        payload = {'identifier': identifier}

        try:
            r = requests.get(\
                self.server_addr + 'homography', params = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if not success:
            return (success, err, data)

        homography = data['homography']
        if file_path:
            path = os.path.join(file_path, 'homography.txt')
            np.savetxt(path, np.array(homography))

        return (success, err, homography)

    def configFiles(self, identifier,
                    max_features_per_frame = None,\
                    num_displacement_frames = None,\
                    min_feature_displacement = None,\
                    max_iterations_to_persist = None,\
                    min_feature_frames = None,\
                    max_connection_distance = None,\
                    max_segmentation_distance = None):

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

        try:
            r = requests.post(self.server_addr + 'config', json = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

    def testConfig(self, identifier, test_flag,
                   frame_start = None,\
                   num_frames = None):

        if not (test_flag == 'feature' or test_flag == 'object'):
            print "ERROR: Invalid flag"
            return (False, 'Invalid test flag: '+str(test_flag))

        success, error_message, status_dict = self.getProjectStatus(identifier)
        if not success:
            return (success, error_message, status_dict)

        if status_dict["homography"]['status'] != 2:
            print "Check your homography and upload (again)."
            return (False, 'Upload homography before testing configuration', None)

        payload = {
            'test_flag': test_flag,
            'identifier': identifier,
            'frame_start': frame_start,
            'num_frames': num_frames
        }

        try:
            r = requests.post(self.server_addr + 'testConfig', json = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

    def getTestConfig(self, identifier, test_flag, file_path):

        payload = {
            'test_flag': test_flag,
            'identifier': identifier
        }

        if test_flag == 'feature':
            file_name = 'feature_video.mp4'
        elif test_flag == 'object':
            file_name = 'object_video.mp4'
        else:
            print "ERROR: Invalid flag"
            return (False, 'Invalid test flag: '+str(test_flag), None)

        try:
            r = requests.get(self.server_addr + 'testConfig', params = payload, stream=True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path,file_name)

        return (success, err, data)

    def defaultConfig(self):
        try:
            r = requests.get(self.server_addr + 'defaultConfig')
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

###############################################################################
# Analysis Functions
###############################################################################

    def analysis(self, identifier, email=None):

        success, error_message, status_dict = self.getProjectStatus(identifier)
        if not success:
            return (success, error_message, status_dict)

        if status_dict["homography"]['status'] != 2:
            print "Check your homography and upload (again)."
            return (False, 'Upload homography before running analysis.', None)

        payload = {
            'identifier': identifier,
            'email': email
        }

        try:
            r = requests.post(self.server_addr + 'analysis', json = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

    def objectTracking(self, identifier, email=None):

        success, error_message, status_dict = self.getProjectStatus(identifier)
        if not success:
            return (success, error_message, status_dict)

        if status_dict["homography"]['status'] != 2:
            print "Check your homography and upload (again)."
            return (False, 'Upload homography before running object tracking.', None)

        payload = {
            'identifier': identifier,
            'email': email
        }

        try:
            r = requests.post(self.server_addr + 'objectTracking', json = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

    def safetyAnalysis(self, identifier, email=None):

        success, error_message, status_dict = self.getProjectStatus(identifier)
        if not success:
            return (success, error_message, status_dict)

        if status_dict["homography"]['status'] != 2:
            print "Check your homography and upload (again)."
            return (False, 'Upload homography before running safety analysis.')
        elif status_dict["object_tracking"]['status'] != 2:
            print "Check object tracking and run (again)."
            return (False, 'Run object tracking before running safety analysis.')

        payload = {
            'identifier': identifier,
            'email': email
        }

        try:
            r = requests.post(self.server_addr + 'safetyAnalysis', json = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)

###############################################################################
# Status Checking Functions
###############################################################################

    def getProjectStatus(self, identifier):

        payload = {
            'identifier': identifier,
        }

        try:
            r = requests.get(self.server_addr + 'status', params = payload)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if not success:
            return (success, err, data)

        status_dict = {}
        for (k,v) in data.iteritems():
            status_dict[k] = {}
            for (key, val) in v.iteritems():
                if key == 'status':
                    status_dict[k][key] = int(val)
                else:
                    status_dict[k][key] = val

        return (True, None, status_dict)

###############################################################################
# Results Functions
###############################################################################

    def results(self, identifier, file_path, ttc_threshold = None):
        print "results called with identifier = {}, ttc_threshold = {}" \
                .format(identifier, ttc_threshold)

        # sync calls
        s, err, data = self.roadUserCounts(identifier,\
                    file_path)
        if not s:
            return (s, err, data)

        s, err, data= self.speedDistribution(identifier,\
                    file_path)
        if not s:
            return (s, err, data)

        s, err, data = self.turningCounts(identifier,\
                    file_path)
        if not s:
            return (s, err, data)

        s, err, data = self.makeReport(identifier,\
                    file_path)
        if not s:
            return (s, err, data)

        # async calls
        s, err, data = self.highlightVideo(identifier,\
                    ttc_threshold)
        if not s:
            return (s, err, data)

        return (True, None, None)

    def highlightVideo(self, identifier, ttc_threshold = None):
        success, error_message, status_dict = self.getProjectStatus(identifier)
        if not success:
            return (success, error_message, status_dict)

        if status_dict["homography"]['status'] != 2:
            print "Check your homography and upload (again)."
            return (False, 'Upload homography before creating a highlight video.')
        elif status_dict["object_tracking"]['status'] != 2:
            print "Check object tracking and run (again)."
            return (False, 'Run object tracking before creating a highlight video.')
        elif status_dict["safety_analysis"]['status'] != 2:
            print "Check safety analysis and run (again)."
            return (False, 'Run safety analysis before creating a highlight video.')

        payload = {
            'identifier': identifier,
            'ttc_threshold': ttc_threshold
        }

        try:
            r = requests.post(self.server_addr + 'highlightVideo', json = payload, stream = True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        return self.parse_error(r)


    def getHighlightVideo(self, identifier, file_path):

        payload = {
            'identifier': identifier
        }

        try:
            r = requests.get(self.server_addr + 'highlightVideo', params = payload, stream = True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path, 'highlight.mp4')

        return (success, err, data)

    def makeReport(self, identifier, file_path):

        payload = {
            'identifier': identifier,
        }

        try:
            r = requests.get(self.server_addr + 'makeReport', params  = payload, stream = True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path, 'santosreport.pdf')

        return (success, err, data)

    def retrieveResults(self, identifier, file_path):

        payload = {
            'identifier': identifier,
        }

        try:
            r = requests.get(self.server_addr + 'retrieveResults', params = payload, stream=True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path, 'results.zip')

        return (success, err, data)

    def roadUserCounts(self, identifier, file_path):

        payload = {
            'identifier': identifier,
        }

        try:
            r = requests.get(self.server_addr + 'roadUserCounts', params = payload, stream=True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path, 'road_user_icon_counts.jpg')

        return (success, err, data)

    def speedDistribution(self, identifier, file_path):

        payload = {
            'identifier': identifier
        }

        try:
            r = requests.get(self.server_addr + 'speedDistribution', params = payload, stream=True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path, 'velocityPDF.jpg')

        return (success, err, data)

    def turningCounts(self, identifier, file_path):
        print "turningCounts called with identifier = {}"\
                .format(identifier)

        payload = {
            'identifier': identifier
        }

        try:
            r = requests.get(self.server_addr + 'turningCounts', params = payload, stream=True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            self.writeToPath(r, file_path, 'turningCounts.jpg')

        return (success, err, data)

###############################################################################
# Compare Methods
###############################################################################

    def compareSpeeds(self, identifier, identifiers_to_cmp, labels_to_cmp, file_path, only_show_85th=False):
        print "compareSpeeds called with identifer = {},\n identifiers_to_cmp = {},\n, labels_to_cmp = {},\n only_show_85th = {}"\
                .format(identifier, identifiers_to_cmp, labels_to_cmp, only_show_85th)

        payload = {
            'identifier': identifier,
            'identifiers_to_cmp': identifiers_to_cmp,
            'labels_to_cmp': labels_to_cmp,
            'only_show_85th': only_show_85th
        }

        try:
            r = requests.get(self.server_addr + 'compareSpeeds', params = payload, stream=True)
        except requests.exceptions.ConnectionError as e:
            return self.connectionError()

        success, err, data = self.parse_error(r)
        if success:
            if only_show_85th:
                self.writeToPath(r, file_path, 'compare85th.jpg')
            else:
                self.writeToPath(r, file_path, 'comparePercentiles.jpg')

        return (success, err, data)


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
        success, err, status_dict = api.getProjectStatus(self.identifier)

        if not success:
            self.callback(err)
            self.stop()
            return

        if self.status_name not in status_dict.keys():
            print(self.status_name + ' not in status dictionary')

        status = status_dict[self.status_name]['status']
        if status == 2:
            print(self.status_name + ' finished!')
            self.stop()
            self.callback(None)
        elif status == 1:
            print(self.status_name + ' is still running')
        elif status == -1:
            print(self.status_name + ' failed')
            if 'failure_message' in status_dict[self.status_name]:
                self.callback(status_dict[self.status_name]['failure_message'])
            else:
                self.callback(self.status_name + ' failed.')
            self.stop()
        else:
            print(self.status_name + ' is not running, not continuing to poll for status')
            self.callback(self.status_name + ' is not running, not continuing to poll for status')
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

###############################################################################
# Run Function on Process with Callback
###############################################################################

class CallbackProcess(object):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={},\
                        callback=None, callback_args=(), callback_kwargs={},\
                        interval=1, timeout=0):

        self._q = Queue()

        self._args = tuple(args)
        self._kwargs = dict(kwargs)
        self._method = self._wrap(target, self._q)
        self._p = Process(target=self._method, group=group, name=name, args=self._args, kwargs=self._kwargs)

        self._callback = callback
        self._callback_args = callback_args
        self._callback_kwargs = callback_kwargs

        self._interval = interval
        self._timeout = timeout
        self._start_time = 0
        self._count = 0

        self._done = False
        self.results = []

    def start(self):
        self._p.start()
        self._start_time=time.time()
        Timer(self._interval,self._check_queue).start()

    # Override to determine what to do when something is grabbed from the queue
    # By default this adds the first value returned from the target function to the results list
    # and sets the internal boolean to be done.
    def on_success(self, data):
        self._done = True
        self.results.append(data)

    # Override to determine when the state in which the callback should be called and the process ended
    # By default this uses a simple internal boolean that is set in the default on_success function.
    def is_done(self):
        return self._done

    # Override to determine what you want the function to do when it finishes
    # By default this calls the provided callback function
    def finish(self):
        if self._callback:
            self._callback(*self._callback_args,**self._callback_kwargs)

    def _wrap(self, func, queue):
        def _function(*args, **kwargs):
            ret = func(*args, **kwargs)
            queue.put(ret)
        return _function

    def _check_queue(self):
        delay = max(self._start_time + (self._count+2)*self._interval - time.time(),0)
        try:
            return_val = self._q.get_nowait()
            self.on_success(data=return_val)
        except EmptyQueue:
            pass
        finally:
            if not self.is_done() and (self._timeout==0 or self._count<self._timeout):
                self._count+=1
                Timer(delay, self._check_queue).start()
            else:
                self._end_process()
                self._q.close()
                self.finish()

    def _end_process(self):
        if self._p.is_alive():
            if self._count>=self._timeout:
                print "Timeout Warning: Process terminating, returned data could be corrupted."
            else:
                print "Warning: Process terminating but was still alive and timeout was not reached, returned data could be corrupted."
            self._p.terminate()
        elif self._p.exitcode == signal.SIGTERM:
            print "Warning: Process was terminated (SIGTERM)"
        elif self._p.exitcode == signal.SIGSEGV:
            print "Warning: Process was terminated (SIGSEGV)"
        elif self._p.exitcode == 0:
            print "Process Exited Cleanly"

class SingleAPICallbackProcess(CallbackProcess):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={},
                        callback=None, callback_args=(), callback_kwargs={},
                        return_data=False, return_error=False, interval=1, timeout=0):

        super(SingleAPICallbackProcess, self).__init__(
                        group=group, target=target, name=name, args=args, kwargs=kwargs,
                        callback=callback, callback_args=callback_args, callback_kwargs=callback_kwargs,
                        interval=interval, timeout=timeout)

        self._return_data = return_data
        self._return_error = return_error

    def finish(self):
        if self._callback:
            if self._return_data:
                try:
                    self._callback(queue=self.results, *self._callback_args, **self._callback_kwargs)
                except TypeError:
                    print "Callback function does not have queue argument. This is required to return data"
            elif self._return_error:
                try:
                    self._callback(error_message=self._get_single_error(), *self._callback_args, **self._callback_kwargs)
                except TypeError:
                    print "Callback function does not have error_message argument. This is required to return the first error message"
            else:
                try:
                    self._callback(*self._callback_args,**self._callback_kwargs)
                except Exception as e:
                    print str(e)

    def _get_single_error(self, index=0):
        if index>=0 and index<len(self.results):
            ret = self.results[index]
            if not ret==None:
                return ret[1]
        return None
