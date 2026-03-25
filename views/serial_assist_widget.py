from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import threading

sys.path.append("../")

from ui.Ui_serial_assist_widget import Ui_SerialAssistWidget
from drivers.driver_serial import *
from views.serial_setting_dialog import SerialSettingDialog
from common import utils


class SerialAssistWidget(QWidget):
    recv_text_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SerialAssistWidget()
        self.ui.setupUi(self)
        self.devices = []
        self.sd: SerialDevice = None

        self.init_ui()
        self.refresh_devices()

    def refresh_devices(self):
        print("扫描设备")
        self.devices = scan_serial_ports()
        print(self.devices)

        self.ui.cb_device.clear()
        for device, description in self.devices:
            text = device if not description else f"{device} - {description}"
            self.ui.cb_device.addItem(text, device)

    def show_setting_dialog(self):
        print("setting")
        dialog = SerialSettingDialog()
        rst = dialog.exec_()
        print(rst)
        if rst == QDialog.Accepted:
            print("accept!")
            print("baud_rate", dialog.baudrate)
            print("data_bits", dialog.data_bits)
            self.ui.cb_baud.setCurrentIndex(self.ui.cb_baud.findText(dialog.baudrate))

    def on_send_clicked(self):
        if self.sd is None:
            print("请先连接设备")
            QMessageBox.warning(self, "警告", "请先连接设备")
            return

        text = self.ui.edit_send.toPlainText()
        if text == "":
            print("请先输入内容再发送")
            QMessageBox.warning(self, "警告", "请先输入要发送的内容")
            return

        self.sd.write(f"{text}\r\n".encode("GBK"))

    def init_ui(self):
        self.ui.btn_refresh.clicked.connect(self.refresh_devices)
        self.ui.btn_setting.clicked.connect(self.show_setting_dialog)
        self.ui.btn_connect.clicked.connect(self.on_connect_clicked)
        self.ui.btn_send.clicked.connect(self.on_send_clicked)
        self.recv_text_signal.connect(self.ui.edit_recv.append)

    def update_connect_ui(self):
        if self.sd is not None:
            self.ui.btn_connect.setText("断开连接(已连接)")
        else:
            self.ui.btn_connect.setText("连接设备")

    def run_serial_assist(self, port, baud_rate):
        self.sd = SerialDevice(port, baud_rate=baud_rate, timeout=0.2)

        success, message = self.sd.open()
        if not success:
            print("连接失败")
            print(message)
            self.sd = None
            self.update_connect_ui()
            return

        print("连接成功, 等待接收数据")
        self.update_connect_ui()

        try:
            while True:
                data = self.sd.read_bytes()
                if data:
                    msg = utils.decode_data(data)
                    print(msg)
                    self.recv_text_signal.emit(msg)
                elif self.sd is None or not self.sd.is_open():
                    break
        except Exception as e:
            print(e)
        finally:
            if self.sd is not None:
                self.sd.close()
            self.sd = None
            self.update_connect_ui()

    def on_connect_clicked(self):
        if self.sd is not None:
            self.sd.close()
            self.sd = None
            self.update_connect_ui()
            return

        if not self.devices:
            QMessageBox.warning(self, "警告", "未扫描到串口设备")
            return

        device = self.devices[self.ui.cb_device.currentIndex()]
        print("connect:", device)
        port = device[0]
        baud_rate = int(self.ui.cb_baud.currentText())
        thread = threading.Thread(target=self.run_serial_assist, args=(port, baud_rate), daemon=True)
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SerialAssistWidget()
    window.show()

    sys.exit(app.exec_())
