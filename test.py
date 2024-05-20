from PyQt5 import QtCore, QtWidgets

class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create main vertical layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        # Create title label and center it
        self.titleLabel = QtWidgets.QLabel("HTML Validator", self.centralwidget)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.mainLayout.addWidget(self.titleLabel)

        # Create horizontal layout for buttons
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.mainLayout.addLayout(self.buttonLayout)

        # Create upload button
        self.uploadButton = QtWidgets.QPushButton("Upload a file", self.centralwidget)
        self.uploadButton.setObjectName("uploadButton")
        self.uploadButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.buttonLayout.addWidget(self.uploadButton)

        # Create download button
        self.downloadButton = QtWidgets.QPushButton("Download errors", self.centralwidget)
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.buttonLayout.addWidget(self.downloadButton)

        # Create horizontal layout for content and errors
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.mainLayout.addLayout(self.horizontalLayout)

        # Create vertical layout for HTML content
        self.htmlLayout = QtWidgets.QVBoxLayout()
        self.htmlLayout.setSpacing(10)
        self.horizontalLayout.addLayout(self.htmlLayout)

        self.htmlContentLabel = QtWidgets.QLabel("HTML Content:", self.centralwidget)
        self.htmlLayout.addWidget(self.htmlContentLabel)

        self.htmlContent = QtWidgets.QTextEdit(self.centralwidget)
        self.htmlContent.setObjectName("htmlContent")
        self.htmlLayout.addWidget(self.htmlContent)

        # Create vertical layout for validation errors
        self.errorLayout = QtWidgets.QVBoxLayout()
        self.errorLayout.setSpacing(10)
        self.horizontalLayout.addLayout(self.errorLayout)

        self.errorContentLabel = QtWidgets.QLabel("Validation Errors:", self.centralwidget)
        self.errorLayout.addWidget(self.errorContentLabel)

        self.errorContentWidget = QtWidgets.QTextEdit(self.centralwidget)
        self.errorContentWidget.setObjectName("errorContentWidget")
        self.errorContentWidget.setReadOnly(True)
        self.errorLayout.addWidget(self.errorContentWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HTML Validator"))
