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
        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)  # Ensures text wrapping

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
        painter.fillRect(event.rect(), QtGui.QColor("#ECECEC"))  # Set a prettier background color for line numbers

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

    def setCustomCursor(self):
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(QtGui.QColor(QtCore.Qt.transparent))
        cursor.setCharFormat(fmt)
        self.setTextCursor(cursor)
        self.cursorPositionChanged.connect(self.updateCursorMarker)

    def updateCursorMarker(self):
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(QtGui.QColor(QtCore.Qt.transparent))
        cursor.setCharFormat(fmt)
        self.setTextCursor(cursor)

        # Draw the custom cursor marker
        cursor_position = self.cursorRect(cursor).center()
        painter = QtGui.QPainter(self.viewport())
        painter.setPen(QtGui.QPen(QtGui.QColor("red"), 2))
        painter.drawLine(cursor_position.x(), cursor_position.y() - 10, cursor_position.x(), cursor_position.y() + 10)


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

        # Create title label and center it
        self.inputLabel = QtWidgets.QLabel("HTML Input", self.centralwidget)
        self.inputLabel.setGeometry(QtCore.QRect(20, 50, 71, 16))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputLabel.setStyleSheet("font-size: 8pt; font-weight: bold; background: none; color: black;")

        # Create title label and center it
        self.outputLabel = QtWidgets.QLabel("Errors Output", self.centralwidget)
        self.outputLabel.setGeometry(QtCore.QRect(870, 50, 80, 16))
        self.outputLabel.setAlignment(Qt.AlignCenter)
        self.outputLabel.setStyleSheet("font-size: 8pt; font-weight: bold; background: none; color: black;")

        # Create upload button
        self.uploadButton = QtWidgets.QToolButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(20, 480, 81, 20))
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
        self.validateButton.setGeometry(QtCore.QRect(440, 480, 81, 20))
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
        self.downloadHTMLButton.setGeometry(QtCore.QRect(740, 480, 100, 20))
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
        self.downloadButton.setGeometry(QtCore.QRect(850, 480, 100, 20))
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
        self.htmlScrollArea.setStyleSheet("""
            QScrollBar:vertical {
                border: 1px solid #CCCCCC;
                background: #F5F5F5;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop: 0 #D3D3D3, stop: 0.5 #C0C0C0, stop: 1 #D3D3D3);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop: 0 #C0C0C0, stop: 0.5 #A9A9A9, stop: 1 #C0C0C0);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.htmlContent = CodeEditor(self.centralwidget)
        self.htmlContent.setStyleSheet("font-size: 8pt; background-color: #fff; color: #000; border: 1px solid #aaa;")
        self.htmlScrollArea.setWidget(self.htmlContent)

        # Create scroll area for validation errors
        self.errorScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.errorScrollArea.setGeometry(QtCore.QRect(510, 70, 441, 391))
        self.errorScrollArea.setWidgetResizable(True)
        self.errorScrollArea.setObjectName("errorScrollArea")

        self.errorContent = QtWidgets.QTextBrowser(self.centralwidget)
        self.errorScrollArea.setWidget(self.errorContent)
        self.errorContent.setStyleSheet(
            "font-size: 10pt; background-color: #fff; border: 1px solid #aaa; border-radius: 4px; color: #000;")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HTML Validator"))
