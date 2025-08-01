import serial as pyserial
import socket
from screen_display import display_on_screen

def read_sensor_data(serial_port='/dev/serial0', baudrate=115200):
    """
    Reads sensor data from a serial port.

    :param serial_port: The serial port to read from.
    :param baudrate: The baud rate for the serial communication.
    :return: A tuple containing AFR and temperature.
    """
    udp_ip = "192.168.1.5"
    udp_port = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ser = pyserial.Serial(serial_port, baudrate, timeout=1)

    try:
        while True:
            if ser.in_waiting >= 8:
                data = ser.read(8)
                afr = data[0] * 0.1
                temperature = data[1]
                message = f"AFR: {afr}, Temperature: {temperature}"
                print(message)
                sock.sendto(message.encode(), (udp_ip, udp_port))
                display_on_screen(afr, temperature)
    except KeyboardInterrupt:
        print("Stopping data read.")
    finally:
        ser.close()

if __name__ == "__main__":
    read_sensor_data()
