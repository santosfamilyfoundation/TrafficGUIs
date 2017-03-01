YOURENVNAME=$1
conda install -n $YOURENVNAME Pillow=2.7.0
conda install -n $YOURENVNAME requests=2.13.0
conda install -n $YOURENVNAME -c menpo opencv=2.4.11
conda install -n $YOURENVNAME pyqt=5.6.0
conda install -n $YOURENVNAME qtawesome=0.4.4
conda install -n $YOURENVNAME nomkl numpy
conda install -n $YOURENVNAME nomkl scipy
conda install -n $YOURENVNAME nomkl scikit-learn
conda install -n $YOURENVNAME nomkl numexpr
conda remove -n $YOURENVNAME mkl mkl-service
conda install -n $YOURENVNAME -c conda-forge requests-toolbelt=0.7.1
