import sys
from qtpy import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Display")
        self.text = QtWidgets.QTextEdit()
        self.disp = QtWidgets.QLabel("Display text:", alignment=QtCore.Qt.AlignCenter)
        self.box = QtWidgets.QGroupBox(alignment=QtCore.Qt.AlignCenter, checked=True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.boxlayout=QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.box)
        self.box.setLayout(self.boxlayout)
        self.boxlayout.addWidget(self.text)
        self.layout.addWidget(self.disp)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.display)

    @QtCore.Slot()
    def display(self):
        self.disp.setText(self.text.toPlainText())
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())