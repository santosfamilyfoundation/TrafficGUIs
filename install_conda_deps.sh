YOURENVNAME=$1

conda env create -f santos_gui_env.yml -n YOURENVNAME
source deactivate
source activate YOURENVNAME
