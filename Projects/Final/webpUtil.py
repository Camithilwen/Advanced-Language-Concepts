# Import PyQt5 GUI libraries
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
)
from PyQt5.QtGui import QPixmap
from WEBPconvert import *
import sys

# Interface
interface = WEBPconvert()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.setWindowTitle("WEBP to PNG Converter")
        self.setGeometry(100, 100, 300, 200)

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Filepath display
        self.filepath = ""
        self.fileDisplay = QLineEdit(self)
        self.fileDisplay.setPlaceholderText("File path will be displayed here")
        self.fileDisplay.setReadOnly(True)
        self.layout.addWidget(self.fileDisplay)

        # Images 
        self.beforeImageLabel = QLabel("Before Image", self)
        self.beforeImageLabel.setFixedSize(300, 300)
        self.layout.addWidget(self.beforeImageLabel)

        self.afterImageLabel = QLabel("After Image", self)
        self.afterImageLabel.setFixedSize(300, 300)
        self.layout.addWidget(self.afterImageLabel)

        # Buttons
        self.openButton = QPushButton("Open", self)
        self.openButton.clicked.connect(self.openCommand)
        self.layout.addWidget(self.openButton)

        self.convertButton = QPushButton("Convert", self)
        self.convertButton.clicked.connect(self.convertCommand)
        self.layout.addWidget(self.convertButton)

        self.closeButton = QPushButton("Close", self)
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

    def openCommand(self):
        """Generates a file dialog and passes selection to the conversion module."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "WEBP files (*.webp);;All Files (*)", options=options)
        if file_path:
            self.filepath = file_path
            self.fileDisplay.setText(file_path)  # Updates the filepath display
            status = interface.fileOpen(file_path)
            if status == "OK":
                pass
                self.displayImage(file_path, self.beforeImageLabel)
            else:
                QMessageBox.information(self, "Error", status)

    def convertCommand(self):
        """Calls the conversion method and generates a save dialog on completion."""
        interface.fileConvert()
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG files (*.png);;All Files (*)", options=options)
        if save_path:
            interface.fileSave(save_path)
            self.displayImage(save_path, self.afterImageLabel)

    def displayImage(self, path, labelWidget):
        """Loads and displays input and output images in their respective label widgets."""
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(300, 300)  # Resizes the image to fit the label
        labelWidget.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
