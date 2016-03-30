# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'safety_main.ui'
#
# Created: Wed Mar 30 07:41:32 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TransportationSafety(object):
    def setupUi(self, TransportationSafety):
        TransportationSafety.setObjectName(_fromUtf8("TransportationSafety"))
        TransportationSafety.resize(1024, 705)
        self.centralWidget = QtGui.QWidget(TransportationSafety)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.main_tab_widget = QtGui.QTabWidget(self.centralWidget)
        self.main_tab_widget.setAcceptDrops(False)
        self.main_tab_widget.setAutoFillBackground(False)
        self.main_tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.main_tab_widget.setElideMode(QtCore.Qt.ElideNone)
        self.main_tab_widget.setTabsClosable(False)
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))
        self.tab_homography = QtGui.QWidget()
        self.tab_homography.setObjectName(_fromUtf8("tab_homography"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_homography)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.control_box = QtGui.QFrame(self.tab_homography)
        self.control_box.setMinimumSize(QtCore.QSize(0, 40))
        self.control_box.setFrameShape(QtGui.QFrame.StyledPanel)
        self.control_box.setFrameShadow(QtGui.QFrame.Raised)
        self.control_box.setObjectName(_fromUtf8("control_box"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.control_box)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.open_buttons = QtGui.QHBoxLayout()
        self.open_buttons.setObjectName(_fromUtf8("open_buttons"))
        self.homography_button_open_camera_image = QtGui.QPushButton(self.control_box)
        self.homography_button_open_camera_image.setObjectName(_fromUtf8("homography_button_open_camera_image"))
        self.open_buttons.addWidget(self.homography_button_open_camera_image)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.open_buttons.addItem(spacerItem)
        self.homography_button_open_aerial_image = QtGui.QPushButton(self.control_box)
        self.homography_button_open_aerial_image.setObjectName(_fromUtf8("homography_button_open_aerial_image"))
        self.open_buttons.addWidget(self.homography_button_open_aerial_image)
        self.verticalLayout_4.addLayout(self.open_buttons)
        self.zoom_sliders = QtGui.QHBoxLayout()
        self.zoom_sliders.setObjectName(_fromUtf8("zoom_sliders"))
        self.homography_label_zoom_camera_image = QtGui.QLabel(self.control_box)
        self.homography_label_zoom_camera_image.setObjectName(_fromUtf8("homography_label_zoom_camera_image"))
        self.zoom_sliders.addWidget(self.homography_label_zoom_camera_image)
        self.homography_hslider_zoom_camera_image = QtGui.QSlider(self.control_box)
        self.homography_hslider_zoom_camera_image.setOrientation(QtCore.Qt.Horizontal)
        self.homography_hslider_zoom_camera_image.setObjectName(_fromUtf8("homography_hslider_zoom_camera_image"))
        self.zoom_sliders.addWidget(self.homography_hslider_zoom_camera_image)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.zoom_sliders.addItem(spacerItem1)
        self.homography_label_zoom_computed_image = QtGui.QLabel(self.control_box)
        self.homography_label_zoom_computed_image.setObjectName(_fromUtf8("homography_label_zoom_computed_image"))
        self.zoom_sliders.addWidget(self.homography_label_zoom_computed_image)
        self.homography_hslider_zoom_computed_image = QtGui.QSlider(self.control_box)
        self.homography_hslider_zoom_computed_image.setOrientation(QtCore.Qt.Horizontal)
        self.homography_hslider_zoom_computed_image.setObjectName(_fromUtf8("homography_hslider_zoom_computed_image"))
        self.zoom_sliders.addWidget(self.homography_hslider_zoom_computed_image)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.zoom_sliders.addItem(spacerItem2)
        self.homography_label_zoom_aerial_image = QtGui.QLabel(self.control_box)
        self.homography_label_zoom_aerial_image.setObjectName(_fromUtf8("homography_label_zoom_aerial_image"))
        self.zoom_sliders.addWidget(self.homography_label_zoom_aerial_image)
        self.homography_hslider_zoom_aerial_image = QtGui.QSlider(self.control_box)
        self.homography_hslider_zoom_aerial_image.setOrientation(QtCore.Qt.Horizontal)
        self.homography_hslider_zoom_aerial_image.setObjectName(_fromUtf8("homography_hslider_zoom_aerial_image"))
        self.zoom_sliders.addWidget(self.homography_hslider_zoom_aerial_image)
        self.verticalLayout_4.addLayout(self.zoom_sliders)
        self.verticalLayout.addWidget(self.control_box)
        self.homography_layout = QtGui.QHBoxLayout()
        self.homography_layout.setObjectName(_fromUtf8("homography_layout"))
        self.homography_cameraview = QtGui.QGraphicsView(self.tab_homography)
        self.homography_cameraview.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.homography_cameraview.setObjectName(_fromUtf8("homography_cameraview"))
        self.homography_layout.addWidget(self.homography_cameraview)
        self.homography_results = QtGui.QGraphicsView(self.tab_homography)
        self.homography_results.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.homography_results.setObjectName(_fromUtf8("homography_results"))
        self.homography_layout.addWidget(self.homography_results)
        self.homography_aerialview = QtGui.QGraphicsView(self.tab_homography)
        self.homography_aerialview.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.homography_aerialview.setObjectName(_fromUtf8("homography_aerialview"))
        self.homography_layout.addWidget(self.homography_aerialview)
        self.verticalLayout.addLayout(self.homography_layout)
        self.homography_flow_control = QtGui.QWidget(self.tab_homography)
        self.homography_flow_control.setMinimumSize(QtCore.QSize(0, 50))
        self.homography_flow_control.setObjectName(_fromUtf8("homography_flow_control"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.homography_flow_control)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.homography_continue_button = QtGui.QPushButton(self.homography_flow_control)
        self.homography_continue_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.homography_continue_button.setObjectName(_fromUtf8("homography_continue_button"))
        self.horizontalLayout_2.addWidget(self.homography_continue_button)
        self.verticalLayout.addWidget(self.homography_flow_control)
        self.main_tab_widget.addTab(self.tab_homography, _fromUtf8(""))
        self.tab_features = QtGui.QWidget()
        self.tab_features.setObjectName(_fromUtf8("tab_features"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_features)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.feature_tracking_parameter_area = QtGui.QScrollArea(self.tab_features)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.feature_tracking_parameter_area.sizePolicy().hasHeightForWidth())
        self.feature_tracking_parameter_area.setSizePolicy(sizePolicy)
        self.feature_tracking_parameter_area.setWidgetResizable(True)
        self.feature_tracking_parameter_area.setObjectName(_fromUtf8("feature_tracking_parameter_area"))
        self.feature_tracking_parameter_widget = QtGui.QWidget()
        self.feature_tracking_parameter_widget.setGeometry(QtCore.QRect(0, 0, 486, 465))
        self.feature_tracking_parameter_widget.setObjectName(_fromUtf8("feature_tracking_parameter_widget"))
        self.feature_tracking_parameter_area.setWidget(self.feature_tracking_parameter_widget)
        self.gridLayout.addWidget(self.feature_tracking_parameter_area, 0, 1, 1, 1)
        self.feature_tracking_video_widget = QtGui.QWidget(self.tab_features)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.feature_tracking_video_widget.sizePolicy().hasHeightForWidth())
        self.feature_tracking_video_widget.setSizePolicy(sizePolicy)
        self.feature_tracking_video_widget.setObjectName(_fromUtf8("feature_tracking_video_widget"))
        self.gridLayout.addWidget(self.feature_tracking_video_widget, 0, 0, 2, 1)
        self.feature_tracking_run_panel = QtGui.QWidget(self.tab_features)
        self.feature_tracking_run_panel.setObjectName(_fromUtf8("feature_tracking_run_panel"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.feature_tracking_run_panel)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.feature_tracking_run_test_progress = QtGui.QProgressBar(self.feature_tracking_run_panel)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.feature_tracking_run_test_progress.sizePolicy().hasHeightForWidth())
        self.feature_tracking_run_test_progress.setSizePolicy(sizePolicy)
        self.feature_tracking_run_test_progress.setProperty("value", 0)
        self.feature_tracking_run_test_progress.setOrientation(QtCore.Qt.Horizontal)
        self.feature_tracking_run_test_progress.setInvertedAppearance(False)
        self.feature_tracking_run_test_progress.setObjectName(_fromUtf8("feature_tracking_run_test_progress"))
        self.horizontalLayout_6.addWidget(self.feature_tracking_run_test_progress)
        self.button_feature_tracking_test = QtGui.QPushButton(self.feature_tracking_run_panel)
        self.button_feature_tracking_test.setObjectName(_fromUtf8("button_feature_tracking_test"))
        self.horizontalLayout_6.addWidget(self.button_feature_tracking_test)
        self.button_feature_tracking_run = QtGui.QPushButton(self.feature_tracking_run_panel)
        self.button_feature_tracking_run.setObjectName(_fromUtf8("button_feature_tracking_run"))
        self.horizontalLayout_6.addWidget(self.button_feature_tracking_run)
        self.gridLayout.addWidget(self.feature_tracking_run_panel, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.feature_tracking_flow_control = QtGui.QFrame(self.tab_features)
        self.feature_tracking_flow_control.setMinimumSize(QtCore.QSize(0, 50))
        self.feature_tracking_flow_control.setFrameShape(QtGui.QFrame.StyledPanel)
        self.feature_tracking_flow_control.setFrameShadow(QtGui.QFrame.Raised)
        self.feature_tracking_flow_control.setObjectName(_fromUtf8("feature_tracking_flow_control"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.feature_tracking_flow_control)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.feature_tracking_back_button = QtGui.QPushButton(self.feature_tracking_flow_control)
        self.feature_tracking_back_button.setObjectName(_fromUtf8("feature_tracking_back_button"))
        self.horizontalLayout_3.addWidget(self.feature_tracking_back_button)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.feature_tracking_continue_button = QtGui.QPushButton(self.feature_tracking_flow_control)
        self.feature_tracking_continue_button.setObjectName(_fromUtf8("feature_tracking_continue_button"))
        self.horizontalLayout_3.addWidget(self.feature_tracking_continue_button)
        self.verticalLayout_3.addWidget(self.feature_tracking_flow_control)
        self.main_tab_widget.addTab(self.tab_features, _fromUtf8(""))
        self.tab_roadusers = QtGui.QWidget()
        font = QtGui.QFont()
        font.setPointSize(17)
        self.tab_roadusers.setFont(font)
        self.tab_roadusers.setObjectName(_fromUtf8("tab_roadusers"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_roadusers)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.object_tracking_placeholder = QtGui.QVBoxLayout()
        self.object_tracking_placeholder.setObjectName(_fromUtf8("object_tracking_placeholder"))
        self.label_object_tracking_msg = QtGui.QLabel(self.tab_roadusers)
        self.label_object_tracking_msg.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_object_tracking_msg.setLineWidth(1)
        self.label_object_tracking_msg.setTextFormat(QtCore.Qt.AutoText)
        self.label_object_tracking_msg.setScaledContents(False)
        self.label_object_tracking_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.label_object_tracking_msg.setObjectName(_fromUtf8("label_object_tracking_msg"))
        self.object_tracking_placeholder.addWidget(self.label_object_tracking_msg)
        self.verticalLayout_6.addLayout(self.object_tracking_placeholder)
        self.main_tab_widget.addTab(self.tab_roadusers, _fromUtf8(""))
        self.tab_results = QtGui.QWidget()
        self.tab_results.setObjectName(_fromUtf8("tab_results"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_results)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.results_grid = QtGui.QGridLayout()
        self.results_grid.setObjectName(_fromUtf8("results_grid"))
        self.results_label0 = QtGui.QLabel(self.tab_results)
        self.results_label0.setAlignment(QtCore.Qt.AlignCenter)
        self.results_label0.setObjectName(_fromUtf8("results_label0"))
        self.results_grid.addWidget(self.results_label0, 0, 0, 1, 1)
        self.results_label2 = QtGui.QLabel(self.tab_results)
        self.results_label2.setAlignment(QtCore.Qt.AlignCenter)
        self.results_label2.setObjectName(_fromUtf8("results_label2"))
        self.results_grid.addWidget(self.results_label2, 1, 1, 1, 1)
        self.results_label1 = QtGui.QLabel(self.tab_results)
        self.results_label1.setAlignment(QtCore.Qt.AlignCenter)
        self.results_label1.setObjectName(_fromUtf8("results_label1"))
        self.results_grid.addWidget(self.results_label1, 1, 0, 1, 1)
        self.results_plot_widget0 = QtGui.QWidget(self.tab_results)
        self.results_plot_widget0.setObjectName(_fromUtf8("results_plot_widget0"))
        self.results_grid.addWidget(self.results_plot_widget0, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.results_grid)
        self.main_tab_widget.addTab(self.tab_results, _fromUtf8(""))
        self.tab_other_tools = QtGui.QWidget()
        self.tab_other_tools.setObjectName(_fromUtf8("tab_other_tools"))
        self.main_tab_widget.addTab(self.tab_other_tools, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.main_tab_widget)
        TransportationSafety.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(TransportationSafety)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuTraffic_Analysis = QtGui.QMenu(self.menuBar)
        self.menuTraffic_Analysis.setObjectName(_fromUtf8("menuTraffic_Analysis"))
        self.menuProject = QtGui.QMenu(self.menuBar)
        self.menuProject.setObjectName(_fromUtf8("menuProject"))
        self.menuHomography_2 = QtGui.QMenu(self.menuProject)
        self.menuHomography_2.setObjectName(_fromUtf8("menuHomography_2"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        TransportationSafety.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(TransportationSafety)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        TransportationSafety.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(TransportationSafety)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        TransportationSafety.setStatusBar(self.statusBar)
        self.actionOpen_Project = QtGui.QAction(TransportationSafety)
        self.actionOpen_Project.setObjectName(_fromUtf8("actionOpen_Project"))
        self.actionAdd_Replace_Video = QtGui.QAction(TransportationSafety)
        self.actionAdd_Replace_Video.setObjectName(_fromUtf8("actionAdd_Replace_Video"))
        self.actionFeature_Tracking = QtGui.QAction(TransportationSafety)
        self.actionFeature_Tracking.setObjectName(_fromUtf8("actionFeature_Tracking"))
        self.actionRoad_User_Tracking = QtGui.QAction(TransportationSafety)
        self.actionRoad_User_Tracking.setObjectName(_fromUtf8("actionRoad_User_Tracking"))
        self.actionLoad_Image = QtGui.QAction(TransportationSafety)
        self.actionLoad_Image.setObjectName(_fromUtf8("actionLoad_Image"))
        self.actionAdd_Replace_Aerial_Image = QtGui.QAction(TransportationSafety)
        self.actionAdd_Replace_Aerial_Image.setObjectName(_fromUtf8("actionAdd_Replace_Aerial_Image"))
        self.actionAdd_Replace_Camera_Image = QtGui.QAction(TransportationSafety)
        self.actionAdd_Replace_Camera_Image.setObjectName(_fromUtf8("actionAdd_Replace_Camera_Image"))
        self.actionCompute_Homography_Performance = QtGui.QAction(TransportationSafety)
        self.actionCompute_Homography_Performance.setObjectName(_fromUtf8("actionCompute_Homography_Performance"))
        self.actionAcquire_Aerial_Image = QtGui.QAction(TransportationSafety)
        self.actionAcquire_Aerial_Image.setObjectName(_fromUtf8("actionAcquire_Aerial_Image"))
        self.actionUser_s_Guide = QtGui.QAction(TransportationSafety)
        self.actionUser_s_Guide.setObjectName(_fromUtf8("actionUser_s_Guide"))
        self.actionAbout = QtGui.QAction(TransportationSafety)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuTraffic_Analysis.addAction(self.actionOpen_Project)
        self.menuHomography_2.addAction(self.actionAdd_Replace_Aerial_Image)
        self.menuHomography_2.addAction(self.actionAdd_Replace_Camera_Image)
        self.menuHomography_2.addSeparator()
        self.menuHomography_2.addAction(self.actionCompute_Homography_Performance)
        self.menuHomography_2.addAction(self.actionAcquire_Aerial_Image)
        self.menuProject.addAction(self.actionAdd_Replace_Video)
        self.menuProject.addAction(self.menuHomography_2.menuAction())
        self.menuProject.addAction(self.actionFeature_Tracking)
        self.menuProject.addAction(self.actionRoad_User_Tracking)
        self.menuHelp.addAction(self.actionUser_s_Guide)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuTraffic_Analysis.menuAction())
        self.menuBar.addAction(self.menuProject.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(TransportationSafety)
        self.main_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TransportationSafety)

    def retranslateUi(self, TransportationSafety):
        TransportationSafety.setWindowTitle(_translate("TransportationSafety", "Transportation Safety", None))
        self.homography_button_open_camera_image.setText(_translate("TransportationSafety", "Open Camera Image", None))
        self.homography_button_open_aerial_image.setText(_translate("TransportationSafety", "Open Aerial Image", None))
        self.homography_label_zoom_camera_image.setText(_translate("TransportationSafety", "Zoom:", None))
        self.homography_label_zoom_computed_image.setText(_translate("TransportationSafety", "Zoom:", None))
        self.homography_label_zoom_aerial_image.setText(_translate("TransportationSafety", "Zoom:", None))
        self.homography_continue_button.setText(_translate("TransportationSafety", " Continue >", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_homography), _translate("TransportationSafety", "Homography", None))
        self.feature_tracking_run_test_progress.setFormat(_translate("TransportationSafety", "%p%", None))
        self.button_feature_tracking_test.setText(_translate("TransportationSafety", "Test on Sample", None))
        self.button_feature_tracking_run.setText(_translate("TransportationSafety", "Run", None))
        self.feature_tracking_back_button.setText(_translate("TransportationSafety", "< Homography", None))
        self.feature_tracking_continue_button.setText(_translate("TransportationSafety", " Continue >", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_features), _translate("TransportationSafety", "Track Features", None))
        self.label_object_tracking_msg.setText(_translate("TransportationSafety", "This wIll look very similar to \"Track Features\".", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_roadusers), _translate("TransportationSafety", "Track Road Users", None))
        self.results_label0.setText(_translate("TransportationSafety", "Data", None))
        self.results_label2.setText(_translate("TransportationSafety", "Look at all the glorious data!", None))
        self.results_label1.setText(_translate("TransportationSafety", "More data", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_results), _translate("TransportationSafety", "Results", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_other_tools), _translate("TransportationSafety", "Other Tools", None))
        self.menuTraffic_Analysis.setTitle(_translate("TransportationSafety", "File", None))
        self.menuProject.setTitle(_translate("TransportationSafety", "Project", None))
        self.menuHomography_2.setTitle(_translate("TransportationSafety", "Homography", None))
        self.menuHelp.setTitle(_translate("TransportationSafety", "Help", None))
        self.actionOpen_Project.setText(_translate("TransportationSafety", "Open Project", None))
        self.actionOpen_Project.setShortcut(_translate("TransportationSafety", "Ctrl+O", None))
        self.actionAdd_Replace_Video.setText(_translate("TransportationSafety", "Video", None))
        self.actionFeature_Tracking.setText(_translate("TransportationSafety", "Feature Tracking", None))
        self.actionRoad_User_Tracking.setText(_translate("TransportationSafety", "Road-User Tracking", None))
        self.actionLoad_Image.setText(_translate("TransportationSafety", "Load Image", None))
        self.actionLoad_Image.setShortcut(_translate("TransportationSafety", "Ctrl+I", None))
        self.actionAdd_Replace_Aerial_Image.setText(_translate("TransportationSafety", "Add/Replace Aerial Image", None))
        self.actionAdd_Replace_Camera_Image.setText(_translate("TransportationSafety", "Add/Replace Camera Image", None))
        self.actionCompute_Homography_Performance.setText(_translate("TransportationSafety", "Compute Homography Performance", None))
        self.actionAcquire_Aerial_Image.setText(_translate("TransportationSafety", "Acquire Aerial Image", None))
        self.actionUser_s_Guide.setText(_translate("TransportationSafety", "User\'s Guide", None))
        self.actionAbout.setText(_translate("TransportationSafety", "About", None))

