from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt


# Custom widget to display line numbers
class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QtCore.QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


# Custom editor widget to show code with line numbers
class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super().__init__(*args)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value //= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QtCore.Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtCore.Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
                                 QtCore.Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlightCurrentLine(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor(QtCore.Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


# Main window layout class
class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(965, 508)  # Make window non-resizable

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create title label and center it
        self.titleLabel = QtWidgets.QLabel("HTML Validator", self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(390, 10, 191, 51))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 18pt; font-weight: bold; background: none; color: black;")

        # Create upload button
        self.uploadButton = QtWidgets.QToolButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(20, 480, 81, 19))
        self.uploadButton.setObjectName("uploadButton")
        self.uploadButton.setText("Upload a file")
        self.uploadButton.setStyleSheet("""
            QToolButton {
                background-color: #ddd;
                color: #000;
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:hover {
                background-color: #ccc;
            }
        """)

        # Create validate button
        self.validateButton = QtWidgets.QToolButton(self.centralwidget)
        self.validateButton.setGeometry(QtCore.QRect(440, 480, 81, 19))
        self.validateButton.setObjectName("validateButton")
        self.validateButton.setText("Validate")
        self.validateButton.setStyleSheet("""
            QToolButton {
                background-color: #ddd;
                color: #000;
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:hover {
                background-color: #ccc;
            }
        """)

        # Create download HTML button
        self.downloadHTMLButton = QtWidgets.QToolButton(self.centralwidget)
        self.downloadHTMLButton.setGeometry(QtCore.QRect(760, 480, 91, 19))
        self.downloadHTMLButton.setObjectName("downloadHTMLButton")
        self.downloadHTMLButton.setText("Download HTML")
        self.downloadHTMLButton.setEnabled(False)
        self.downloadHTMLButton.setStyleSheet("""
            QToolButton:disabled {
                background-color: #f5f5f5;
                color: #aaa;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:enabled {
                background-color: #ddd;
                color: #000;
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:enabled:hover {
                background-color: #ccc;
            }
        """)

        # Create download button
        self.downloadButton = QtWidgets.QToolButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(860, 480, 91, 19))
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.setText("Download errors")
        self.downloadButton.setStyleSheet("""
            QToolButton {
                background-color: #ddd;
                color: #000;
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:hover {
                background-color: #ccc;
            }
        """)

        # Create scroll area for HTML content
        self.htmlScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.htmlScrollArea.setGeometry(QtCore.QRect(20, 70, 441, 391))
        self.htmlScrollArea.setWidgetResizable(True)
        self.htmlScrollArea.setObjectName("htmlScrollArea")

        self.htmlContent = CodeEditor(self.centralwidget)
        self.htmlContent.setStyleSheet("background-color: #fff; color: #000; border: 1px solid #aaa;")
        self.htmlScrollArea.setWidget(self.htmlContent)

        # Create scroll area for validation errors
        self.errorScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.errorScrollArea.setGeometry(QtCore.QRect(510, 70, 441, 391))
        self.errorScrollArea.setWidgetResizable(True)
        self.errorScrollArea.setObjectName("errorScrollArea")

        self.errorContent = QtWidgets.QTextBrowser(self.centralwidget)
        self.errorScrollArea.setWidget(self.errorContent)
        self.errorContent.setStyleSheet(
            "background-color: #fff; border: 1px solid #aaa; border-radius: 4px; color: #000;")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HTML Validator"))
