#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
cd ..
echo $DIR
pyinstaller -distpath=$DIR -workpath=$DIR $DIR/app.spec
chmod 777 $DIR/dist/app

echo “[Press any button to exit]”
read -rsn1
exit