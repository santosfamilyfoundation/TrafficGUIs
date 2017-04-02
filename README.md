# SantosGUI

GUI application(s) for interfacing with TrafficIntelligence and related code.

SantosGUI is currently supported on Ubuntu 14.04 and Windows 8,10.

### Table of Contents

- [Installation](#installation)
- [Packaging Application](#packaging-application)

## Installation

### Repo Cloning

Clone the repo with:
```
git clone https://github.com/santosfamilyfoundation/SantosGUI
```

### Conda Installation

The recommended way to run this project is using Anaconda.

#### Download

##### Windows

You can install Anaconda from [here](https://www.continuum.io/downloads#windows). Be sure to install the Python 2.7 version. Install it to `C:\Anaconda2`.

##### Linux

You can install Anaconda from [here](https://www.continuum.io/downloads#linux). Be sure to install the Python 2.7 version. Then open Terminal, cd to the `Downloads` folder, and run: `bash Anaconda2-x.x.x-Linux-x86[_64].sh`. You can use the default `/home/USER/anaconda2/` folder.

#### Create Conda Environment

Run the following command to create a conda environment that we will use for this project:

```
conda create -n santosgui
```

### OpenCV Installation

##### Windows

Download OpenCV 2.4.13 for Windows from [here](https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.13/opencv-2.4.13.exe/download). Run it and extract to `C:\opencv`.

Next, we have to copy the `cv2.pyd` file. Find the file at either `C:\opencv\build\python\2.7\x86` on 32-bit systems or `C:\opencv\build\python\2.7\x64` on 64-bit systems. Then copy `cv2.pyd` to `C:\Anaconda2\envs\santosgui\Lib\site-packages`.

Next, open the Control Panel and search 'environment variables'. Then click "Edit the system environment variables". Click "Environment Variables". Create a variable named `OPENCV_DIR` and set its value to `C:\opencv\build\x64\vc12` (use `x86` instead of `x64` on 32-bit systems). Then add `%OPENCV_DIR%\bin` and `C:\opencv\sources\3rdparty\ffmpeg` to your PATH variable.

##### Linux

Simply run:
```
sudo apt-get install python-opencv
```

#### Python Dependency Installation

You need to install the following dependencies using conda. If using Git Bash, run `bash install_conda_deps.sh santosgui` to install all packages. Otherwise, run all of the lines from the `install_conda_deps.sh` file, with `santosgui` instead of `$YOURENVNAME`. For example:

```
conda env create -f santos_gui_env.yml -n santosgui
source deactivate
source activate santosgui
```

#### Video Codec Installation

In order for Qt to play videos on Windows, you will need to install video codecs. This is a known problem and intended behavior of Qt, as seen [here](https://bugreports.qt.io/browse/QTBUG-51692). Installing the codec [here](http://www.codecguide.com/download_k-lite_codec_pack_basic.htm) will fix this issue. You can leave all of the default settings (but be sure not to install their bloatware!).

## Packaging Application

Simply run the `SantosBuild.sh` file in `application/packaging` directory of SantosGUI with: `bash SantosBuild.sh`. The executable will be output to the `application/dist` folder.
