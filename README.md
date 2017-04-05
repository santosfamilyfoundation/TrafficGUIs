# SantosGUI

GUI application(s) for interfacing with TrafficIntelligence and related code.

SantosGUI is currently supported on Ubuntu 14.04 and Windows 8,10.

## Table of Contents

- [Installation](#installation)
  - [Conda Installation](#conda-installation)
  - [Install Dependencies](#install-dependencies)
  - [OpenCV Installation (Windows Only)](#opencv-installation-windows-only)
  - [Video Codec Installation (Windows Only)](#video-codec-installation-windows-only)
- [Running](#running)
- [Packaging Application](#packaging-application)

## Installation

### Conda Installation

First, we have to install conda and dependencies. Follow the directions for Unix, or Windows.

#### Unix Installation

The recommended way to run this project on Unix is using Miniconda. You can install Miniconda from [here](https://conda.io/miniconda.html). Be sure to install the Python 2.7 version. Install it to `~/miniconda2` when prompted and let the installer prepend the location to your PATH. Install with `bash Miniconda2-latest-Linux-x86_64.sh`, DO NOT USE `sudo`. 

For the next steps, you may need to restart Terminal, or reload `~/.bashrc` by executing `. ~/.bashrc`.

#### Windows Installation

The recommended way to run this project on Windows is using Anaconda. You can install Anaconda from [here](https://www.continuum.io/downloads#windows). Be sure to install the Python 2.7 version. Install it to `C:\Anaconda2`.

### Install Dependencies

Next, you have two options: [installing dependencies from YML (recommended)](#install-dependencies-from-yml), or [installing dependencies from script](#install-dependencies-from-script). You can follow these instructions if you have a bash shell (i.e. are on Unix, or are on Windows and have either Git Bash or Windows Subsystem for Linux).

If you are on Windows and don't have a Bash shell, you will have to run the instructions yourself (or install Git Bash). This means that when we say run `bash install_conda_deps.sh santosgui`, that means to:

1. Open the file `install_conda_deps.sh` in a text editor.
2. Replace `$YOURENVNAME` with `santosgui`.
3. Copy all of the lines from the file (excluding `YOURENVNAME=$1`) into the command prompt.

#### Install Dependencies from YML

Run the following command to create and activate the conda environment for the project:

```
bash install_conda_deps.sh santosgui
```

#### Install Dependencies from Script

Run the following command to begin installing the various dependencies of the project. The last

```
bash build_conda_deps.sh santosgui
```

### OpenCV Installation (Windows Only)

#### Windows Installation

Download OpenCV 2.4.13 for Windows from [here](https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.13/opencv-2.4.13.exe/download). Run it and extract to `C:\opencv`.

Next, we have to copy the `cv2.pyd` file. Find the file at either `C:\opencv\build\python\2.7\x86` on 32-bit systems or `C:\opencv\build\python\2.7\x64` on 64-bit systems. Then copy `cv2.pyd` to `C:\Anaconda2\envs\santosgui\Lib\site-packages`.

Next, open the Control Panel and search 'environment variables'. Then click "Edit the system environment variables". Click "Environment Variables". Create a variable named `OPENCV_DIR` and set its value to `C:\opencv\build\x64\vc12` (use `x86` instead of `x64` on 32-bit systems). Then add `%OPENCV_DIR%\bin` and `C:\opencv\sources\3rdparty\ffmpeg` to your PATH variable.


### Video Codec Installation (Windows Only)

In order for Qt to play videos on Windows, you will need to install video codecs. This is a known problem and intended behavior of Qt, as seen [here](https://bugreports.qt.io/browse/QTBUG-51692). Installing the codec [here](http://www.codecguide.com/download_k-lite_codec_pack_basic.htm) will fix this issue. You can leave all of the default settings (but be sure not to install their bloatware!).

## Running

To run, activate the conda env with:

```bash
source activate santosgui # Bash shell
activate santosgui # Windows Command Prompt
```

Then `cd` into the `application` folder and run:

```
python app.py
```

(Note: Currently, this must be run from the application/ directory).

## Packaging Application

Simply run the `SantosBuild.sh` file in `application/packaging` directory of SantosGUI with: `bash SantosBuild.sh`. The executable will be output to the `application/dist` folder.

