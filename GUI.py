import sys

from PyQt5 import QtWidgets

from main import validate_html
from ui_layout import UiMainWindow


class HTMLValidatorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)  # Set up the UI from the file

        # Connect buttons to methods
        self.ui.uploadButton.clicked.connect(self.upload_file)
        self.ui.validateButton.clicked.connect(self.validate_html_ui)
        self.ui.downloadHTMLButton.clicked.connect(self.download_html)
        self.ui.downloadButton.clicked.connect(self.download_errors)

    def upload_file(self):
        # Open a file dialog to select a file
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open HTML file", "",
                                                             "HTML Files (*.html);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                html = file.read()
            # Display the content in a text widget
            self.ui.htmlContent.setPlainText(html)
            # Immediately validate the HTML content
            self.validate_html_ui()

    def validate_html_ui(self):
        html_content = self.ui.htmlContent.toPlainText()
        errors = validate_html(html_content)

        if isinstance(errors, list):
            error_text = "\n".join(errors)
            self.ui.errorContent.setPlainText(error_text)
        else:
            self.ui.errorContent.setPlainText(errors)

    def download_errors(self):
        # Logic to download the error report
        errors = self.ui.errorContent.toPlainText()
        if errors:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Error Report", "",
                                                                 "Text Files (*.txt);;All Files (*)")
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(errors)

    def download_html(self):
        # Logic to download the error report
        html = self.ui.htmlContent.toPlainText()
        if html:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save HTML code", "",
                                                                 "HTML Files (*.html);;Text Files (*.txt);"
                                                                 ";All Files (*)")
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(html)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = HTMLValidatorApp()
    main_window.show()  # Makes window visible
    sys.exit(app.exec_())  # Starts application's main loop
