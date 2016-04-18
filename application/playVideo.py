#! /usr/bin/env python

import sys, argparse

import storage, cvutils, utils

from numpy.linalg.linalg import inv
from numpy import loadtxt
from app_config import AppConfig as ac
from cvutils import *

parser = argparse.ArgumentParser(description='The program displays feature or object trajectories overlaid over the video frames.', epilog = 'Either the configuration filename or the other parameters (at least video and database filenames) need to be provided.')
parser.add_argument('--cfg', dest = 'configFilename', help = 'name of the configuration file')
parser.add_argument('-d', dest = 'databaseFilename', help = 'name of the Sqlite database file')
parser.add_argument('-i', dest = 'videoFilename', help = 'name of the video file')
parser.add_argument('-t', dest = 'trajectoryType', help = 'type of trajectories to display', choices = ['feature', 'object'], default = 'feature')
parser.add_argument('-o', dest = 'homographyFilename', help = 'name of the image to world homography file')
parser.add_argument('--intrinsic', dest = 'intrinsicCameraMatrixFilename', help = 'name of the intrinsic camera file')
parser.add_argument('--distortion-coefficients', dest = 'distortionCoefficients', help = 'distortion coefficients', nargs = '*', type = float)
parser.add_argument('--undistorted-multiplication', dest = 'undistortedImageMultiplication', help = 'undistorted image multiplication', type = float)
parser.add_argument('-u', dest = 'undistort', help = 'undistort the video (because features have been extracted that way)', action = 'store_true')
parser.add_argument('-f', dest = 'firstFrameNum', help = 'number of first frame number to display', type = int)
parser.add_argument('-r', dest = 'rescale', help = 'rescaling factor for the displayed image', default = 1., type = float)
parser.add_argument('-s', dest = 'nFramesStep', help = 'number of frames between each display', default = 1, type = int)
parser.add_argument('--save-images', dest = 'saveAllImages', help = 'save all images', action = 'store_true')
parser.add_argument('--last-frame', dest = 'lastFrameNum', help = 'number of last frame number to save (for image saving, no display is made)', type = int)
parser.add_argument('--output', dest = 'outputVideoPath', help='outputVideoPath')

args = parser.parse_args()

if args.configFilename: # consider there is a configuration file
    params = storage.ProcessParameters(args.configFilename)
    videoFilename = params.videoFilename
    databaseFilename = params.databaseFilename
    if params.homography is not None:
        homography = inv(params.homography)
    else:
        homography = None
    intrinsicCameraMatrix = params.intrinsicCameraMatrix
    distortionCoefficients = params.distortionCoefficients
    undistortedImageMultiplication = params.undistortedImageMultiplication
    undistort = params.undistort
    firstFrameNum = params.firstFrameNum
    outputVideoPath = parser.outputVideoPath
else:
    homography = None
    undistort = False
    intrinsicCameraMatrix = None
    distortionCoefficients = []
    undistortedImageMultiplication = None
    firstFrameNum = 0

if not args.configFilename and args.videoFilename is not None:
    videoFilename = args.videoFilename
if not args.configFilename and args.databaseFilename is not None:
    databaseFilename = args.databaseFilename
if not args.configFilename and args.homographyFilename is not None:
    homography = inv(loadtxt(args.homographyFilename))            
if not args.configFilename and args.intrinsicCameraMatrixFilename is not None:
    intrinsicCameraMatrix = loadtxt(args.intrinsicCameraMatrixFilename)
if not args.configFilename and args.distortionCoefficients is not None:
    distortionCoefficients = args.distortionCoefficients
if not args.configFilename and args.undistortedImageMultiplication is not None:
    undistortedImageMultiplication = args.undistortedImageMultiplication
if args.firstFrameNum is not None:
    firstFrameNum = args.firstFrameNum

   
objects = storage.loadTrajectoriesFromSqlite(databaseFilename, args.trajectoryType)
boundingBoxes = storage.loadBoundingBoxTableForDisplay(databaseFilename)
makeVideo(videoFilename, objects, boundingBoxes, homography, firstFrameNum, args.lastFrameNum, rescale = args.rescale, nFramesStep = args.nFramesStep, saveAllImages = args.saveAllImages, undistort = (undistort or args.undistort), intrinsicCameraMatrix = intrinsicCameraMatrix, distortionCoefficients = distortionCoefficients, undistortedImageMultiplication = undistortedImageMultiplication, writeVideo = True, outputVideoPath)

def makeVideo(videoFilename, objects, boundingBoxes = {}, homography = None, firstFrameNum = 0, lastFrameNumArg = None, printFrames = True, rescale = 1., nFramesStep = 1, saveAllImages = False, undistort = False, intrinsicCameraMatrix = None, distortionCoefficients = None, undistortedImageMultiplication = 1., annotations = [], gtMatches = {}, toMatches = {},writeVideo=True, outputVideoPath):
    '''Displays the objects overlaid frame by frame over the video '''
    from moving import userTypeNames
    from math import ceil, log10

    capture = cv2.VideoCapture(videoFilename)
    width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.cv.CV_FOURCC('D','I','V','X')
    outputVideo = cv2.VideoWriter(outputVideoPath,fourcc, 30.0, (width,height))
    #outputVideo = cv2.VideoWriter('~/Documents/laurier/testVideo.avi', cv2.cv.CV_FOURCC('H','2','6','4'),30,(704,384),True)

    windowName = 'frame'
    if rescale == 1.:
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)

    if undistort: # setup undistortion
        [map1, map2] = computeUndistortMaps(width, height, undistortedImageMultiplication, intrinsicCameraMatrix, distortionCoefficients)
    if capture.isOpened():
        key = -1
        ret = True
        frameNum = firstFrameNum
        capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, firstFrameNum)
        if lastFrameNumArg is None:
            from sys import maxint
            lastFrameNum = maxint
        else:
            lastFrameNum = lastFrameNumArg
        nZerosFilename = int(ceil(log10(lastFrameNum)))
        objectToDeleteIds = []
        while ret and not quitKey(key) and frameNum <= lastFrameNum:
            ret, img = capture.read()
            if ret:
                if undistort:
                    img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)
                if printFrames:
                    print('frame {0}'.format(frameNum))
                if len(objectToDeleteIds) > 0:
                    objects = [o for o in objects if o.getNum() not in objectToDeleteIds]
                    objectToDeleteIds = []
                # plot objects
                for obj in objects:
                    if obj.existsAtInstant(frameNum):
                        if obj.getLastInstant() == frameNum:
                            objectToDeleteIds.append(obj.getNum())
                        if not hasattr(obj, 'projectedPositions'):
                            if homography is not None:
                                obj.projectedPositions = obj.positions.project(homography)
                            else:
                                obj.projectedPositions = obj.positions
                        cvPlot(img, obj.projectedPositions, cvColors[obj.getNum()], frameNum-obj.getFirstInstant())
                        if frameNum not in boundingBoxes.keys() and obj.hasFeatures():
                            imgcrop, yCropMin, yCropMax, xCropMin, xCropMax = imageBox(img, obj, frameNum, homography, width, height)
                            cv2.rectangle(img, (xCropMin, yCropMin), (xCropMax, yCropMax), cvBlue, 1)
                        objDescription = '{} '.format(obj.num)
                        if userTypeNames[obj.userType] != 'unknown':
                            objDescription += userTypeNames[obj.userType][0].upper()
                        if len(annotations) > 0: # if we loaded annotations, but there is no match
                            if frameNum not in toMatches[obj.getNum()]:
                                objDescription += " FA"
                        cv2.putText(img, objDescription, obj.projectedPositions[frameNum-obj.getFirstInstant()].asint().astuple(), cv2.cv.CV_FONT_HERSHEY_PLAIN, 1, cvColors[obj.getNum()])
                # plot object bounding boxes
                if frameNum in boundingBoxes.keys():
                    for rect in boundingBoxes[frameNum]:
                        cv2.rectangle(img, rect[0].asint().astuple(), rect[1].asint().astuple(), cvColors[obj.getNum()])
                # plot ground truth
                if len(annotations) > 0:
                    for gt in annotations:
                        if gt.existsAtInstant(frameNum):
                            if frameNum in gtMatches[gt.getNum()]:
                                color = cvColors[gtMatches[gt.getNum()][frameNum]] # same color as object
                            else:
                                color = cvRed
                                cv2.putText(img, 'Miss', gt.topLeftPositions[frameNum-gt.getFirstInstant()].asint().astuple(), cv2.cv.CV_FONT_HERSHEY_PLAIN, 1, cvRed)
                            cv2.rectangle(img, gt.topLeftPositions[frameNum-gt.getFirstInstant()].asint().astuple(), gt.bottomRightPositions[frameNum-gt.getFirstInstant()].asint().astuple(), color)
                # saving images and going to next
                if not saveAllImages:
                    cvImshow(windowName, img, rescale)
                    #key = cv2.waitKey()
                if saveAllImages or saveKey(key):
                    cv2.imwrite('image-{{:0{}}}.png'.format(nZerosFilename).format(frameNum), img)
                if writeVideo:
                    outputVideo.write(img)
                frameNum += nFramesStep
                if nFramesStep > 1:
                    capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNum)
        cv2.destroyAllWindows()
    else:
        print 'Cannot load file ' + videoFilename