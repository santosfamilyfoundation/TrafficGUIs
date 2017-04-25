import cloud_api as api

TEST_IP = 'localhost'
VIDEO_PATH = 'path/to/video'
project_path = 'path/to/local/project/'
UNIT_PIXEL_RATIO = 0.05

#TODO: Remove raw_input hotfix in favor of checking function call

#SAMPLE POINTS PROVIDED
AERIAL_PTS = [
            (1002.2857055664062, 388.0),
            (864.7857055664062, 575.5),
            (1061.2142333984375, 389.78570556640625),
            (1036.2142333984375, 291.5714416503906),
            (757.6428833007812, 575.5),
            (843.3571166992188, 391.5714416503906)]
CAMERA_PTS = [
            (508.5128173828125, 231.58973693847656),
            (941.8461303710938, 416.20513916015625),
            (493.1282043457031, 146.974365234375),
            (316.20513916015625, 216.2051239013672),
            (1000.8204956054688, 611.076904296875),
            (577.7435913085938, 503.3846130371094)]

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
    identifier = None # set if you have already uploaded video
    if identifier is None:
        identifier = remote.uploadVideo(VIDEO_PATH)
        raw_input('Uploading Video, please wait...\n Press Enter to Continue')

    ###########################################################################
    # Upload Mask
    ###########################################################################
    mask_path = None
    if mask_path:
        remote.uploadMask(identifier, mask_path)
        raw_input('Uploading Mask, please wait...\n Press Enter to Continue')

    # ###########################################################################
    # # Configure Homography
    # ###########################################################################
    remote.configHomography(identifier, UNIT_PIXEL_RATIO, AERIAL_PTS, CAMERA_PTS)
    raw_input('Configuring Homography, please wait...\n Press Enter to Continue')

    # ###########################################################################
    # # Test Configs
    # ###########################################################################

    remote.configFiles(identifier,\
                max_features_per_frame = 1001,\
                num_displacement_frames = 11,\
                min_feature_displacement = 0.000099,\
                max_iterations_to_persist = 201,\
                min_feature_frames = 14,\
                max_connection_distance = 0.99,\
                max_segmentation_distance = 0.69)
    raw_input('Updating Config Files, please wait...\n Press Enter to Continue')

    remote.testConfig('feature', identifier)
    raw_input('Testing Feature Config, please wait...\n Press Enter to Continue')

    remote.testConfig('object', identifier)
    raw_input('Testing object Config, please wait...\n Press Enter to Continue')

    # ###########################################################################
    # # Run Analysis Routes
    # ###########################################################################

    run_separately = False
    if run_separately:
        remote.objectTracking(identifier,EMAIL)
        raw_input('Running Object Tracking, please wait...\n Press Enter to Continue')

        remote.safetyAnalysis(identifier,EMAIL)
        raw_input('Running Safety Analysis, please wait...\n Press Enter to Continue')
    else:
        remote.analysis(identifier,EMAIL)
        raw_input('Running Analysis, please wait...\n Press Enter to Continue')

    # ###########################################################################
    # # Run Result Routes
    # ###########################################################################

    remote.highlightVideo(identifier)
    raw_input('Generating Highlight Video, please wait...\n Press Enter to Continue')

    remote.roadUserCounts(identifier, project_path)
    raw_input('Generating User Counts, please wait...\n Press Enter to Continue')

    remote.speedDistribution(identifier, project_path)
    raw_input('Generating Speed Distribution, please wait...\n Press Enter to Continue')

    remote.turningCounts(identifier, project_path)
    raw_input('Generating Turning Counts, please wait...\n Press Enter to Continue')

    remote.makeReport(identifier)
    raw_input('Generating Report, please wait...\n Press Enter to Continue')

    remote.retrieveResults(identifier, project_path)
    raw_input('Retrieving Results, please wait...\n Press Enter to Continue')
