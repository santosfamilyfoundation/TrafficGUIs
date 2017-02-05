import cloud_api as api

TEST_IP = 'localhost'
VIDEO_PATH = 'path/to/video'
AERIAL_PATH = 'path/to/aerial/image'
CAMERA_PATH = 'path/to/camera/image'
UNIT_PIXEL_RATIO = 0.05

#SAMPLE POINTS PROVIDED
AERIAL_PTS = [
            (695.7036743164062, 406.8148193359375),
            (819.7777709960938, 240.1481475830078),
            (856.8148193359375, 553.111083984375),
            (830.888916015625, 390.1481628417969),
            (932.74072265625, 397.5555419921875)]
CAMERA_PTS = [
            (614.2222290039062, 703.111083984375),
            (936.4444580078125, 419.77777099609375),
            (197.55555725097656, 630.888916015625),
            (519.7777709960938, 330.8888854980469),
            (558.6666870117188, 536.4444580078125)]

EMAIL = None

if __name__ == '__main__':
    print "Syntax looks fine!"

    ###########################################################################
    # Setup CloudWizard
    ###########################################################################
    remote = api.CloudWizard(TEST_IP)

    ###########################################################################
    # Upload Video
    ###########################################################################
    id = remote.uploadVideo(VIDEO_PATH)['identifier']

    ###########################################################################
    # Upload Homography
    ###########################################################################
    remote.uploadHomography(\
            AERIAL_PATH, CAMERA_PATH,\
            id, UNIT_PIXEL_RATIO, AERIAL_PTS, CAMERA_PTS)


    ###########################################################################
    # Test Configs
    ###########################################################################
 
    remote.configFiles(id,\
                max_features_per_frame = 1001,\
                num_displacement_frames = 11,\
                min_feature_displacement = 0.000099,\
                max_iterations_to_persist = 201,\
                min_feature_frames = 14,\
                max_connection_distance = 0.99,\
                max_segmentation_distance = 0.69)
    remote.testConfig('object', id)
    remote.testConfig('feature', id)

    ###########################################################################
    # Run Analysis Route
    ###########################################################################
    remote.analysis(id,EMAIL)
    #remote.objectTracking(id,EMAIL)
    #remote.safetyAnalysis(id,EMAIL)

