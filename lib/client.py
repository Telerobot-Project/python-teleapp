import socket
import struct
from struct import calcsize
import threading
from lib.video import Video
from lib.robot import Robot


class Client:
    def __init__(self, user_video: Video, usb_video: Video, tof_video: Video, robot: Robot):
        self.host = '192.168.43.161'  # '192.168.1.189'
        self.port = 5050
        self.addr = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.run = True

        self.user_video = user_video
        self.usb_video = usb_video
        self.tof_video = tof_video
        self.robot = robot

        self.data = b''
        self.send_buffer = b''
        self.payload_size = struct.calcsize("Q")

    def start(self):
        self.start_thread = threading.Thread(target=self.start_connection)
        self.start_thread.start()

    def start_connection(self):
        self.connected = False
        print('Connecting to server...')
        self.socket.connect(self.addr)
        print('Connected to server')
        self.connected = True

        self.read_thread = threading.Thread(target=self.read_loop)
        self.read_thread.start()

        self.send_thread = threading.Thread(target=self.send_loop)
        self.send_thread.start()

    def read_loop(self):
        while self.run:
            try:
                self.receive_data()
                self.receive_video(self.usb_video)

                self.usb_video.unpack()
            except:
                pass

    def send_loop(self):
        while self.run:
            try:
                if self.user_video.new_data:
                    self.send_data()
                    self.user_video.new_data = False
            except:
                pass

    def receive_data(self):
        while len(self.data) < calcsize("iiiiiii"):
            self.data += self.socket.recv(4*1024)

        self.robot.gyro, self.robot.us[0], self.robot.us[1], self.robot.us[2], self.robot.us[3], self.robot.us[4], self.robot.us[5] = struct.unpack(
            "iiiiiii", self.data[:calcsize("iiiiiii")])
        self.data = self.data[calcsize("iiiiiii"):]

    def receive_video(self, video_obj: Video):
        while len(self.data) < self.payload_size:
            self.data += self.socket.recv(4*1024)

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.socket.recv(4*1024)

        video_obj.binary = self.data[:msg_size]
        self.data = self.data[msg_size:]

    def send_data(self):
        self.user_video.get_binary()

        self.send_buffer = b''
        self.send_buffer += struct.pack('iii', self.robot.speed,
                                        self.robot.direction, self.robot.turn_speed)
        self.send_buffer += struct.pack("Q", len(self.user_video.binary))
        self.send_buffer += self.user_video.binary

        self.socket.sendall(self.send_buffer)

    def close(self):
        self.run = False
        self.connected = False
        self.socket.close()
