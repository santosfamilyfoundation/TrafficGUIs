
import sys
from PyQt4 import QtGui
import io
import ConfigParser
from PyQt4.QtGui import *
 

#adding mask to tacking.cfg causes type errors 
#----------------------------------------------------------------------

# Create an PyQT4 application object.
a = QApplication(sys.argv) 

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = QWidget()

# Get filename using QFileDialog
path = QFileDialog.getOpenFileName(w, 'Open File', '/') 
path1= str(path)

class gui(QtGui.QWidget):

    
    def __init__(self):
        super(gui, self).__init__()
        
        self.initUI()
        

    def initUI(self): 

        self.btn = QtGui.QPushButton('Set Config', self)
        # self.btn.move(20, 20)
        self.btn.clicked.connect(self.createConfig)
        
        self.label1 = QtGui.QLabel("first frame to process")
        # input box 
        self.input1 = QtGui.QLineEdit()

        self.label2 = QtGui.QLabel("number of frames to process")
        # self.label1.move(130, 22)
        self.input2 = QtGui.QLineEdit()
        # self.le.move(150, 22)

        self.label3 = QtGui.QLabel("maximum connection-distance")
        self.input3 = QtGui.QLineEdit()

        self.label4 = QtGui.QLabel("maximum segmentation-distance")
        self.input4 = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.label1, 1, 0)
        grid.addWidget(self.input1, 1, 1)

        grid.addWidget(self.label2, 2, 0)
        grid.addWidget(self.input2, 2, 1)

        grid.addWidget(self.label3, 3, 0)
        grid.addWidget(self.input3, 3, 1)

        grid.addWidget(self.label4, 4, 0)
        grid.addWidget(self.input4, 4, 1)

        grid.addWidget(self.btn, 5, 0)

        self.setLayout(grid) 
        
        # window box location and size 
        self.setGeometry(500, 100, 550, 150)

        self.setWindowTitle('Input config')
        self.show()
        
       

    def createConfig(self,path):
        """
        Create a config file
        """
        config = ConfigParser.ConfigParser()

# add new content to config file 
        config.add_section("added")
        config.set("added", "frame1", self.input1.text())
        config.set("added", "nframes", self.input2.text())
        config.set("added", "mm-connection-distance", self.input3.text())
        config.set("added", "mm-segmentation-distance", self.input4.text())
        # config.remove_section("added")

        # opens a file for writing      
        # with open(path,"wb") as config_file:

        # opens a file for appending 
        with open(path1,"a") as config_file:
            config.write(config_file)

# to remove the section header from config file  

        #opens the file to read      
        f = open(path1,"r")
        lines = f.readlines()
        f.close()
        #opens the file to write 
        f = open(path1,"w")
        for line in lines:
            #removes the section header 
            if line!="[added]"+"\n":
                f.write(line)
        f.close()

         
def main():
    app = QtGui.QApplication(sys.argv)
    ex = gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

  

