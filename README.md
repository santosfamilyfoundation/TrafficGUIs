# SantosGUI

SantosGUI is a desktop application that interfaces with [SantosCloud](https://github.com/santosfamilyfoundation/SantosCloud) in order to analyze videos of intersections and produce traffic safety metrics.

SantosGUI allows users to create projects, upload videos, and configure projects, in order to have intersections of interest analyzed. This GUI makes the appropriate API calls to SantosCloud in order to have videos analyzed, and then displays the results of the analysis to the user.

SantosGUI is currently supported on modern versions of Windows, macOS, and 64-bit Ubuntu.

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

First, we have to install conda and dependencies. Follow the directions for Unix, or Windows. (Unix includes macOS).

#### Unix Installation

The recommended way to run this project on Unix is using Miniconda. You can install Miniconda from [here](https://conda.io/miniconda.html). Be sure to install the Python 2.7 version. Install it to `~/miniconda2` when prompted and let the installer prepend the location to your PATH. Install with `bash Miniconda2-latest-Linux-x86_64.sh`, DO NOT USE `sudo`.

For the next steps, you may need to restart Terminal, or reload `~/.bashrc` by executing `. ~/.bashrc`.

#### Windows Installation

The recommended way to run this project on Windows is using Anaconda. You can install Anaconda from [here](https://www.continuum.io/downloads#windows). Be sure to install the Python 2.7 version. Install it to `C:\Anaconda2`.

### Install Dependencies

Next, you must install dependencies. These instructions install dependencies using `conda` into a conda environment that you must run the project in. If you follow these instructions, it will create an environment named 'santosgui'. You can replace the name 'santosgui' with any other name throughout these instructions.

#### Bash Shell

You can follow these instructions if you have a bash shell (i.e. are on Unix, or are on Windows and have either Git Bash or Windows Subsystem for Linux). Run the following command to create and activate the conda environment for the project:

```
bash install_conda_deps.sh santosgui
```

#### Windows Command Prompt

If you are on Windows and don't have a Bash shell, you will have to create the conda environment yourself (or install Git Bash). To do this, run the following command:

```
conda env create -f envs/env_windows.yml -n santosgui
```

#### Install Dependencies from Script

Run the following command to begin installing the various dependencies of the project. The last

```
bash build_conda_deps.sh santosgui
```

### Video Codec Installation

#### Windows

In order for Qt to play videos on Windows, you will need to install video codecs. This is a known problem and intended behavior of Qt, as seen [here](https://bugreports.qt.io/browse/QTBUG-51692). Installing the codec [here](http://www.codecguide.com/download_k-lite_codec_pack_basic.htm) will fix this issue. You can leave all of the default settings (but be sure not to install their bloatware!).

#### Ubuntu/Debian

To install codecs for playing movies, run the following commands from command line:

```
sudo apt-get install gstreamer1.0-libav gstreamer1.0-plugins-bad-videoparsers
```

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

After running, you can deactivate the conda environment with:

```bash
source deactivate # Bash shell
deactivate # Windows Command Prompt
```

## Packaging Application

Simply run the `SantosBuild.sh` file in `application/packaging` directory of SantosGUI with: `bash SantosBuild.sh`. The executable will be output to the `application/dist` folder.

