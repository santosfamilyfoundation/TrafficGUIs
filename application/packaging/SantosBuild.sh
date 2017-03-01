#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
cd ..
echo $DIR
pyinstaller -distpath=$DIR $DIR/app.spec
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Finding the current os type"
echo
if [ "$(uname)" == "Darwin" ]; then
    echo "Mac OS X platform"  
    chmod 777 dist/SantosTrafficAnalysis
    dmgbuild -s build_settings.py -D app=dist/SantosTrafficAnalysis "Santos Analysis" Santos.dmg
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "GNU/Linux platform"
    chmod 777 dist/SantosTrafficAnalysis
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "Windows NT platform"
    chmod 777 dist/SantosTrafficAnalysis.exe
fi

echo “[Press any button to exit]”
read -rsn1
exit