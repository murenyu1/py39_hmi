import serial
from serial import Serial
from serial.tools import list_ports


def scan_serial_ports():
    ports = list_ports.comports()
    return [(port.device, port.description) for port in ports]


class SerialDevice:
    def __init__(self, port, baud_rate=9600, timeout=None):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial: Serial = None

    def open(self):
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            if self.serial.is_open:
                return True, f"Serial port {self.port} opened successfully."
        except serial.SerialException as e:
            print("Failed to open serial port:", str(e))
            return False, str(e)

        return False, f"Serial port {self.port} open failed."

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Serial port closed.")
        else:
            print("Serial port is not open.")

    def write(self, data):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None

        try:
            self.serial.write(data)
            print("Data written:", data)
        except serial.SerialException as e:
            print("Failed to write data:", str(e))

    def flush(self):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None

        self.serial.flush()

    def read(self, num_bytes):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None
        try:
            return self.serial.read(num_bytes)
        except serial.SerialException as e:
            print("Failed to read data:", str(e))

        return None

    def read_bytes(self):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None
        try:
            size = self.serial.in_waiting
            if size <= 0:
                size = 1
            return self.serial.read(size)
        except serial.SerialException as e:
            print("Failed to read data:", str(e))

        return None

    def readline(self):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None

        try:
            return self.serial.readline()
        except Exception as e:
            print("Failed to read data:", str(e))

        return None

    def is_open(self):
        if not self.serial:
            return False

        return self.serial.is_open


if __name__ == "__main__":
    serial_ports = scan_serial_ports()
    if len(serial_ports) > 0:
        print("Available serial ports:")
        for device, description in serial_ports:
            print(device, "-->", description)
    else:
        print("No serial ports found.")
