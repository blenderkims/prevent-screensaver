from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import resources

class MainWindow(QtWidgets.QMainWindow):
    ES_AWAYMODE_REQUIRED = 0x00000040
    ES_CONTINUOUS = 0x80000000
    ES_DISPLAY_REQUIRED = 0x00000002
    ES_SYSTEM_REQUIRED = 0x00000001
    PROGRAM = 'Prevent Screensaver Program'
    ACTIVATED = 'Prevent Screensaver Activation'
    DEACTIVATED = 'Prevent Screensaver Deactivation'

    def __init__(self):
        super().__init__()
        self.settings()

    def settings(self):
        # MainWindow Settings
        self.setObjectName("MainWindow")
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.setEnabled(True)
        self.setFixedSize(442, 80)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

        # QWidget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Grid Layout
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 441, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")

        # Enable Button
        self.enableButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enableButton.sizePolicy().hasHeightForWidth())
        self.enableButton.setSizePolicy(sizePolicy)
        self.enableButton.setObjectName("enableButton")
        self.enableButton.clicked.connect(self.enableButtonClick)
        self.gridLayout.addWidget(self.enableButton, 0, 0, 1, 1)

        # Disable Button
        self.disableButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disableButton.sizePolicy().hasHeightForWidth())
        self.disableButton.setSizePolicy(sizePolicy)
        self.disableButton.setObjectName("disableButton")
        self.disableButton.clicked.connect(self.disableButtonClick)
        self.gridLayout.addWidget(self.disableButton, 0, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)

        # StatusBar
        self.statusbar = QtWidgets.QStatusBar(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.showMessage("Program Starting...")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # System Tray Settings
        self.trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(":/icons/icon.png"))
        self.trayIcon.setToolTip(self.PROGRAM)
        self.contextMenu = QtWidgets.QMenu()
        self.enableAction = self.contextMenu.addAction(self.ACTIVATED)
        self.enableAction.setIcon(QtGui.QIcon(":/icons/on.png"))
        self.enableAction.triggered.connect(self.enableButtonClick)
        self.disableAction = self.contextMenu.addAction(self.DEACTIVATED)
        self.disableAction.setIcon(QtGui.QIcon(":/icons/off.png"))
        self.disableAction.triggered.connect(self.disableButtonClick)
        self.exitAction = self.contextMenu.addAction("Program Exit")
        self.exitAction.setIcon(QtGui.QIcon(":/icons/shutdown.png"))
        self.exitAction.triggered.connect(QtWidgets.qApp.quit)
        self.trayIcon.setContextMenu(self.contextMenu)
        self.trayIcon.activated.connect(self.trayIconActivated)
        self.trayIcon.show()

        # Timer Settings (5 seconds)
        QtCore.QTimer.singleShot(5000, self.trayEvent)
        self.messageBox = QtWidgets.QMessageBox(self)
        self.messageBox.setWindowTitle("Program Information")
        self.messageBox.setText("After 5 seconds, it will move to the system tray.")
        self.messageBox.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", self.PROGRAM))
        self.enableButton.setText(_translate("MainWindow", self.ACTIVATED))
        self.disableButton.setText(_translate("MainWindow", self.DEACTIVATED))

        # ChangeEvent override

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowState.WindowMinimized:
                self.hide()

    def trayEvent(self):
        self.messageBox.close()
        self.setWindowState(QtCore.Qt.WindowState.WindowMinimized)

    def enableButtonClick(self):
        ctypes.windll.kernel32.SetThreadExecutionState(
            MainWindow.ES_DISPLAY_REQUIRED | MainWindow.ES_AWAYMODE_REQUIRED | MainWindow.ES_SYSTEM_REQUIRED | MainWindow.ES_CONTINUOUS)
        self.enableButton.setDisabled(True)
        self.disableButton.setDisabled(False)
        self.enableAction.setDisabled(True)
        self.disableAction.setDisabled(False)
        self.statusbar.showMessage(self.ACTIVATED)

    def disableButtonClick(self):
        ctypes.windll.kernel32.SetThreadExecutionState(MainWindow.ES_CONTINUOUS)
        self.enableButton.setDisabled(False)
        self.disableButton.setDisabled(True)
        self.enableAction.setDisabled(False)
        self.disableAction.setDisabled(True)
        self.statusbar.showMessage(self.DEACTIVATED)

    def trayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isHidden():
                self.showNormal()
            else:
                self.hide()