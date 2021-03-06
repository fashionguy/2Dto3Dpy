import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtGui
import cv2
from vtk import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.image_path = ""
        self.image = ""
        self.label_image = QLabel(self)
        self.frame_model = QFrame(self)
        # self.label_model = QLabel(self)
        self.label_image_width = 400
        self.label_image_height = 400
        self.ui()  # 添加菜单栏，可以打开本地图片


    def ui(self):
        menubar = self.menuBar()
        menu = menubar.addMenu("菜单")
        open_image = QAction("打开图片", self)
        open_image.setShortcut("Ctrl+Q")
        open_image.setStatusTip('open an picture')
        menu.addAction(open_image)
        open_image.triggered.connect(self.open_image)

        self.label_image.setText("显示图片")
        self.label_image.setFixedSize(self.label_image_width, self.label_image_height)
        # self.label_image.move(0, menubar.height())
        self.label_image.setStyleSheet("QLabel{background:white;}")

        # self.label_model.setText("显示模型")
        # self.label_model.setFixedSize(self.label_image_width, self.label_image_height)
        # self.label_model.setStyleSheet("QLabel{background:white;}")

        vl = QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor()
        vl.addWidget(vtkWidget)
        self.ren = vtkRenderer()
        self.ren.SetBackground(0.01, 0.2, 0.01)
        vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()

        self.iren.Initialize()
        self.frame_model.setLayout(vl)

        hbox = QHBoxLayout()
        hbox.addWidget(self.label_image)
        hbox.addWidget(self.frame_model)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        layout_widget = QWidget()
        layout_widget.setLayout(vbox)
        self.setCentralWidget(layout_widget)
        self.setGeometry(300, 300, 1000, 500)
        self.setWindowTitle('2Dto3D')
        self.show()

    def load_obj(self, path):
        # Create source
        filename = path
        reader = vtkOBJReader()
        reader.SetFileName(filename)
        reader.Update()

        # Create a mapper
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        actor = vtkActor()

        actor.SetMapper(mapper)

        self.ren.AddActor(actor)
        self.ren.ResetCamera()


    def open_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "Image files(*.jpg *.png)")
        self.image = cv2.imread(self.image_path)
        self.show_image()
        self.process_image()

    def show_image(self):
        height, width = self.image.shape[0], self.image.shape[1]

        if height > width:
            self.label_image.setFixedSize(self.label_image_width * width / height, self.label_image_height)
        else:
            self.label_image.setFixedSize(self.label_image_width, self.label_image_height * height / width)
        print(self.label_image.width(), self.label_image.height())
        img = QtGui.QPixmap(self.image_path).scaled(self.label_image.width(), self.label_image.height())
        self.label_image.setPixmap(img)

    def process_image(self):
        pass

    def closeEvent(self, ev):
        reply = QMessageBox.question(self, 'Message', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            ev.accept()
        else:
            ev.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
