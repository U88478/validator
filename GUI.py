import sys

from PyQt5 import QtWidgets

from main import validate_html
from ui_layout import UiMainWindow


class HTMLValidatorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.ui.htmlContent.setCustomCursor()  # Set the custom cursor

        self.original_html = ""
        self.content_changed_after_upload = False

        self.ui.htmlContent.textChanged.connect(self.on_html_content_changed)
        self.ui.uploadButton.clicked.connect(self.upload_file)
        self.ui.validateButton.clicked.connect(self.validate_html_ui)
        self.ui.downloadHTMLButton.clicked.connect(self.download_html)
        self.ui.downloadButton.clicked.connect(self.download_errors)

    def on_html_content_changed(self):
        # Enable the download HTML button if content has changed after a new file upload
        if self.ui.htmlContent.toPlainText() != self.original_html:
            self.content_changed_after_upload = True
            self.ui.downloadHTMLButton.setEnabled(True)
        else:
            self.ui.downloadHTMLButton.setEnabled(False)

    def upload_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open HTML file", "",
                                                             "HTML Files (*.html);;Text Files (*.txt);;All Files (*)",
                                                             options=options)
        if file_name:
            with open(file_name, 'r') as file:
                html = file.read()
            self.ui.htmlContent.setPlainText(html)
            self.original_html = html
            self.content_changed_after_upload = False  # Reset the flag after uploading a new file
            self.validate_html_ui()

    def validate_html_ui(self):
        html_content = self.ui.htmlContent.toPlainText()
        errors = validate_html(html_content)
        if isinstance(errors, list):
            self.ui.errorContent.setPlainText("\n".join(errors))
        else:
            self.ui.errorContent.setPlainText(errors)
        self.original_html = html_content  # Update original_html after validation
        self.ui.downloadHTMLButton.setEnabled(True)  # Enable button after validation

    def download_html(self):
        # Logic to download the HTML content
        html_content = self.ui.htmlContent.toPlainText()
        if html_content:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save HTML", "",
                                                                 "HTML Files (*.html);;Text Files (*.txt);;"
                                                                 "All Files (*)")
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(html_content)

    def download_errors(self):
        errors = self.ui.errorContent.toPlainText()
        if errors:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Error Report", "",
                                                                 "Text Files (*.txt);;All Files (*)")
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(errors)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = HTMLValidatorApp()
    main_window.show()  # Makes window visible
    sys.exit(app.exec_())  # Starts application's main loop
