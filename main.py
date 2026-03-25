"""
PyQt5版GUI工具
"""


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.Ui_main_window import Ui_MainWindow
import sys
from views.serial_assist_widget import SerialAssistWidget
from views.serial_setting_dialog import SerialSettingDialog

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 创建对象
        self.ui = Ui_MainWindow()
        # 初始化内容
        self.ui.setupUi(self)
        # 初始化ui
        self.init_ui()

    def init_ui(self):
        pass
        
        
    def init_ui(self):
        self.ui.tabWidget.addTab(SerialAssistWidget(self),"串口助手")
        self.ui.tabWidget.addTab(SerialAssistWidget(self),"飞控状态")
        self.ui.tabWidget.addTab(SerialAssistWidget(self),"飞控设置")
        
        self.ui.tabWidget.setCurrentIndex(0) #默认打开的页面

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
