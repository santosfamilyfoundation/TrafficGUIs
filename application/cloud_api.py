###This will hold all api calls for TrafficCloud
import os
import pickle
import uuid

def CloudWizard(api_type,project_path,*arg):
    print arg
    if api_type == 'server':
        print "SERVER"
        return TrafficCloud_Server(project_path,arg[0])
    if api_type == 'local':
        print "LOCAL"
        return TrafficCloud_Local(project_path)

class TrafficCloud_Abstract:

    def __init__(self,project_path):
        #TODO: Needs to be done in sync with server
        #   not a uuid creation
        self._ids = self.readIds()
        self.project_path = project_path
        self._ids[self.project_path] = uuid.uuid4()
        self._writeIds()

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

    def uploadFiles(self, types, paths, callback):
        raise NotImplementedError("uploadFiles not yet implemented")

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

class TrafficCloud_Local(TrafficCloud_Abstract):
    def __init__(self,project_path):
        TrafficCloud_Abstract.__init__(self, project_path)


class TrafficCloud_Server(TrafficCloud_Abstract):
    def __init__(self,project_path,s_ip):
        TrafficCloud_Abstract.__init__(self, project_path)
        if s_ip == 'localhost':
            self.server_ip = '127.0.0.1'
        else:
            self.server_ip = s_ip

#FOR TESTING PURPOSES ONLY
if __name__ == '__main__':
    server = CloudWizard('server',"/project/path/server",'192.168.1.1')
    local_server = CloudWizard('server',"/project/path/local_server",'localhost')
    local = CloudWizard('local',"/project/path/local")
    #server = TrafficCloud_Server("/project/path/goes/ahere","localhost")
    print server.server_ip
    print server.readIds()
    print local_server.server_ip
    print local_server.readIds()
    print local.readIds()