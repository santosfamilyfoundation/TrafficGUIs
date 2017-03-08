YOURENVNAME=$1

conda install -n $YOURENVNAME Pillow=2.7.0
conda install -n $YOURENVNAME requests=2.13.0
conda install -n $YOURENVNAME -c menpo opencv=2.4.11
conda install -n $YOURENVNAME pyqt=5.6.0
conda install -n $YOURENVNAME qtawesome=0.4.4
conda install -n $YOURENVNAME nomkl numpy=1.12.0
conda install -n $YOURENVNAME nomkl scipy=0.18.1
conda install -n $YOURENVNAME nomkl scikit-learn=0.18.1
conda install -n $YOURENVNAME nomkl numexpr=2.6.2
conda remove -n $YOURENVNAME mkl mkl-service
conda install -n $YOURENVNAME -c conda-forge requests-toolbelt=0.7.1
conda install -n $YOURENVNAME libpng=1.6.22