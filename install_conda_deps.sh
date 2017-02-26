YOURENVNAME=$1
conda install -n $YOURENVNAME Pillow=2.7.0
conda install -n $YOURENVNAME requests=2.13.0
conda install -n $YOURENVNAME -c menpo opencv=2.4.11
conda install -n $YOURENVNAME pyqt=5.6.0
conda install -n $YOURENVNAME qtawesome=0.4.4
conda install -n $YOURENVNAME nomkl numpy scipy scikit-learn numexpr
conda remove -n $YOURENVNAME mkl mkl-service
