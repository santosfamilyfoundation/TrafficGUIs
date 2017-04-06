
YOURENVNAME=$1

conda remove -y --all -n $YOURENVNAME

if [[ "$OSTYPE" == "linux-gnu" ]] || [[ "$OSTYPE" == "darwin"* ]]; then
	# Linux or macOS install
	echo "Detected Unix; Installing dependencies..."
	conda env create -f envs/env_unix.yml -n $YOURENVNAME

elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
	# Some form of windows
	echo "Detected Windows; Installing dependencies..."
	conda env create -f envs/env_windows.yml -n $YOURENVNAME

else
	# Unknown.
	echo "Unknown OS; You will have to install dependencies manually."
	exit 1

fi

source deactivate
source activate $YOURENVNAME

