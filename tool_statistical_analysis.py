import sys
import vtk
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
from fury import window,actor
from PyQt5.QtWidgets import QPushButton,QAction, QMenu, QApplication, QFileDialog,QWidget,QSplitter,QTableWidget,QTableWidgetItem

from dipy.data import fetch_bundles_2_subjects, read_bundles_2_subjects
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from dipy.tracking.streamline import transform_streamlines, length


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FingureCanvas
from matplotlib.figure import Figure

#import AFQ.segmentation as seg

from dipy.tracking import utils
interactive = False  # set to True to show the interactive display window

class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        
        Qt.QMainWindow.__init__(self, parent)

        ####################### menubar###############
        title = "Embed Matplotlib In PyQt5"
#        top = 400
#        left = 400
#        width = 900
#        height = 500
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        newAct = QAction('Track File', self)                
        fileMenu.addAction(newAct)        
        newAct.triggered.connect(self.openFileNameDialog)
        
      
        newAct = QAction('FA File', self)                
        fileMenu.addAction(newAct)        
        newAct.triggered.connect(self.openFileNameDialog_fa)
        
        
        self.setWindowTitle(title)
        #self.setGeometry(top,left, width, height)
              
        ####################### Pyqt############### 
        
        ########## frame##################
        self.frame = Qt.QFrame()
        
        self.createTable()

        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        
        
        
        #############Button#########################
        button_length = QPushButton('Length', self)
        button_length.clicked.connect(self.on_click_length)
        self.vl.addWidget(button_length)
        
        button_afq = QPushButton('AFQ', self)
        button_afq.clicked.connect(self.on_click_afq)
        self.vl.addWidget(button_afq)
        
        #############Button#########################
        
       
        self.layoutVertical = Qt.QVBoxLayout(self)
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        
        self.vl.addWidget(self.tableWidget) 
        self.setLayout(self.vl)
        self.show()

    def on_click_length(self):
         print("Histogram...")
         lengths = list(length(wholeTract))
         fig_hist, ax = plt.subplots()

         
         ax.hist(lengths, color='burlywood')
         ax.set_xlabel('Length')
         ax.set_ylabel('Count')
         
        
         plt.show()
         
         
    def on_click_afq(self):
         print('PyQt5 button click')     
         FA_img = nib.load(fileName_fa)
         FA_data = FA_img.get_data()
         
         print ('Done')
 
                  
#         profile = seg.calculate_tract_profile(FA_data,  wholeTract.tolist())        
#         fig, ax = plt.subplots(1)
#         ax.plot(profile)
#         plt.show()

        
    
    def openFileNameDialog(self):
        global fileName_trk 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName_trk , _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Track Files (*.trk)", options=options)
        if fileName_trk:
             self.load_streamline(fileName_trk)
           
   
    def openFileNameDialog_fa(self):
        global fileName_fa 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Image Files (*.nii.gz)", options=options)
        if fileName:
             self.load_streamline(fileName_fa)         
       
 
    def load_streamline(self,fileName_trk):
        print(fileName_trk)
        global wholeTract
        from fury import window
        scene = window.Scene()
        
        affine=utils.affine_for_trackvis(voxel_size=np.array([1.25,1.25,1.25]))

        wholeTract= nib.streamlines.load(fileName_trk)
        wholeTract = wholeTract.streamlines        
        wholeTract_transform = transform_streamlines(wholeTract, np.linalg.inv(affine))
        stream_actor = actor.line(wholeTract_transform)

        #scene.set_camera(position=(-176.42, 118.52, 128.20),
        #         focal_point=(113.30, 128.31, 76.56),
        #         view_up=(0.18, 0.00, 0.98))   
        scene.add(stream_actor)
        
        self.vtkWidget.GetRenderWindow().AddRenderer(scene)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()
        
        
    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Maximum FA value"))
        self.tableWidget.setItem(0,1, QTableWidgetItem(""))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Minimum FA value"))
        self.tableWidget.setItem(1,1, QTableWidgetItem(""))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Maximum Length value"))
        self.tableWidget.setItem(2,1, QTableWidgetItem(""))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Minimum Length value"))
        self.tableWidget.setItem(3,1, QTableWidgetItem(""))
        self.tableWidget.setItem(4,0, QTableWidgetItem("Voxel Count"))
        self.tableWidget.setItem(4,1, QTableWidgetItem(""))
        
        self.tableWidget.move(0,0)

        # table selection change
        #self.tableWidget.doubleClicked.connect(self.on_click)
   
if __name__ == "__main__":
    
    app = Qt.QApplication(sys.argv)
    
    window = MainWindow()
    
    
    sys.exit(app.exec_())
    
    sys.exit(app.exec_())
