import constant
import serial
import socket
import json


class SerialConnector:
    @classmethod
    def receive(self, arduino_serial):
        return arduino_serial.readline()

    @classmethod
    def get_connection(self):
        return serial.Serial(constant.DEVICE_NAME, constant.BAUD_RATE)


class UDPConnector:
    @classmethod
    def send(self, value, dstip, dstport, mysocket):
        mysocket.sendto(value, (dstip, dstport))

    @classmethod
    def get_dstip(self):
        return constant.IP_ADDRESS

    @classmethod
    def get_dstport(self):
        return constant.PORT_NUMBER

    @classmethod
    def make_mysocket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class SensorDataReceiver:
    @classmethod
    def set_sender(self, mysocket):
        return mysocket.recvfrom(self.get_buffer_size())

    @classmethod
    def get_json_data(self, string):
        return json.loads(string.decode(constant.STRING_CODE))

    @classmethod
    def get_port_number(self):
        return constant.PORT_NUMBER

    @classmethod
    def get_host_name(self):
        return constant.HOST_NAME

    @classmethod
    def get_buffer_size(self):
        return constant.BUFFER_SIZE

    @classmethod
    def make_mysocket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @classmethod
    def bind_mysocket(self, mysocket):
        return mysocket.bind((self.get_host_name(), self.get_port_number()))


class HapticDataReceiver(SensorDataReceiver):
    @classmethod
    def receive_sensor_data(self, mysocket):
        string, addr = self.set_sender(mysocket)
        json_data = self.get_json_data(string)
        data = self.change_data_to_angle(self.get_socket_data(json_data))
        return data

    @classmethod
    def get_socket_data(self, json_data):
        return json_data[constant.SOCKET]

    @classmethod
    def change_data_to_angle(self, data):
        value = float(data) - constant.MIN_PRESSURE
        angle = constant.MAX_ANGLE - constant.MIN_ANGLE
        pressuer = constant.MAX_PRESSURE - constant.MIN_PRESSURE
        data = value * angle / pressuer + constant.MIN_ANGLE
        if data <= constant.MIN_PRESSURE:
            return constant.MIN_ANGLE
        if data >= constant.MAX_ANGLE:
            return constant.MAX_ANGLE
        return int(data)


class BicycleDataReceiver(SensorDataReceiver):
    @classmethod
    def receive_sensor_data(self, mysocket):
        string, addr = self.set_sender(mysocket)
        json_data = self.get_json_data(string)
        speed = self.change_speed_to_eight_bit(self.get_speed_data(json_data))
        wind = self.change_wind_to_eight_bit(self.get_wind_data(json_data))
        return [speed, wind]

    @classmethod
    def receive_speed_data(self, mysocket):
        string, addr = self.set_sender(mysocket)
        json_data = self.get_json_data(string)
        speed = self.change_speed_to_eight_bit(self.get_speed_data(json_data))
        return speed

    @classmethod
    def receive_wind_data(self, mysocket):
        string, addr = self.set_sender(mysocket)
        json_data = self.get_json_data(string)
        wind = self.change_wind_to_eight_bit(self.get_wind_data(json_data))
        return wind

    @classmethod
    def get_speed_data(self, json_data):
        return json_data[constant.SPEED]

    @classmethod
    def get_wind_data(self, json_data):
        return json_data[constant.WIND]

    @classmethod
    def change_speed_to_eight_bit(self, data):
        data = data * (constant.MAX_EIGHT_BIT / constant.MAX_SPEED)
        if data >= constant.MAX_EIGHT_BIT:
            return constant.MAX_EIGHT_BIT
        return int(data)

    @classmethod
    def change_wind_to_eight_bit(self, data):
        data = data * (constant.MAX_EIGHT_BIT / constant.MAX_WIND)
        if data >= constant.MAX_EIGHT_BIT:
            return constant.MAX_EIGHT_BIT
        return int(data)
