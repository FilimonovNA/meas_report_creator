from PyQt5.QtWidgets import *
import sys
from const import *

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupWindow()
       # self.folder = self.user_path
    #    self.selectPathWithData()

    def setupWindow(self):
        self.setWindowTitle("Report creator ver 2.0")
        self.move(300,300)
        self.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
    #     self.lbl = QLabel('Test label', self)
    #     self.lbl.move(30, 30)
    #     self.nemo_path_label = QLabel('Выберите папку \n с файлами', self)
    #     self.nemo_path_label.move(10, 10)
    #     self.nemo_path_label.setFixedSize(150, 30)
    #     self.select_data_button = QPushButton("Выбрать", self)
    #     self.select_data_button.setFixedSize(50, 20)
    #     self.select_data_button.move(10, 170)
    #     self.select_data_button.setCheckable(True)
    #     self.select_data_button.clicked.connect(self.selectPathWithData)

    def selectPathWithData(self):
        self.user_path = str(QFileDialog.getExistingDirectory(None, "Выберите папку с "
                                                                    "файлами из Nemo"))

    def info_from_user(self, text, y_position):
        self.x_position = 10
        self.label = QLabel(text)
        self.label.move(self.x_position, y_position)
        self.label.setFixedSize(200, 200)
        # self.lbl.setMargin(10)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.info_from_user('Hello', 70)
    win.show()
    sys.exit(app.exec_())
