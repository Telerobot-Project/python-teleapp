"""A socket client for communicating with the robot via a binary protocol.

Packets received from the robot have the following structure:
    int        : gyroscope measurement
    int[6]     : ultrasonic sensor measurements
    ulong long : size of the video data
    ...        : video data

Packets sent to the robot have the following structure:
    int        : robot movement speed
    int        : robot direction
    int        : robot rotation speed
    ulong long : size of the video data
    ...        : video data

"""

import logging
import socket
import struct
import threading
from struct import calcsize
from typing import NamedTuple

from .robot import Robot
from .video import Video


class ConnectionInfo(NamedTuple):
    """IP address and port of the robot."""

    host: str = "localhost"
    port: int = 5050


class RobotVideo(NamedTuple):
    """A bundle of camera video and ToF video from the robot."""

    camera: Video
    tof: Video


class Client:
    """A socket client for communicating with the robot via a binary protocol."""

    def __init__(
        self,
        user_video: Video,
        robot_video: RobotVideo,
        robot: Robot,
        host: ConnectionInfo,
    ) -> None:
        """Initialize the socket client."""
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run = True

        self.user_video = user_video
        self.robot_video = robot_video
        self.robot = robot

        self.data = b""

        threading.Thread(target=self.__start_connection).start()

    def __start_connection(self) -> None:
        """Connect to the robot."""
        logging.info("Connecting to server...")
        self.socket.connect(self.host)
        logging.info("Connected to server")

        threading.Thread(target=self.__read_loop).start()
        threading.Thread(target=self.__send_loop).start()

    def __read_loop(self) -> None:
        """Loop that receives data from the robot."""
        while self.run:
            try:
                self.__receive_data()
                self.__receive_video(self.robot_video.camera)

                self.robot_video.camera.unpack()
            except Exception:
                logging.exception("Error while running the read loop")

    def __receive_data(self) -> None:
        """Receive robot state (location, rotation, etc)."""
        data_size = calcsize("iiiiiii")

        while len(self.data) < data_size:
            self.data += self.socket.recv(16 * 1024)

        (
            self.robot.gyro,
            self.robot.us[0],
            self.robot.us[1],
            self.robot.us[2],
            self.robot.us[3],
            self.robot.us[4],
            self.robot.us[5],
        ) = struct.unpack("iiiiiii", self.data[:data_size])
        self.data = self.data[data_size:]

    def __receive_video(self, video: Video) -> None:
        """Receive camera video from the robot."""
        header_size = struct.calcsize("Q")

        while len(self.data) < header_size:
            self.data += self.socket.recv(16 * 1024)

        video_size = struct.unpack("Q", self.data[:header_size])[0]
        self.data = self.data[header_size:]

        while len(self.data) < video_size:
            self.data += self.socket.recv(16 * 1024)

        video.binary = self.data[:video_size]
        self.data = self.data[video_size:]

    def __send_loop(self) -> None:
        """Loop that sends data to the robot."""
        while self.run:
            try:
                if self.user_video.new_data:
                    self.__send_data()
                    self.user_video.new_data = False
            except Exception:
                logging.exception("Error while running the send loop")

    def __send_data(self) -> None:
        """Send user video over the socket."""
        self.user_video.pack()

        packet = struct.pack(
            "iii",
            self.robot.speed,
            self.robot.direction,
            self.robot.turn_speed,
        )
        packet += struct.pack("Q", len(self.user_video.binary))
        packet += self.user_video.binary

        self.socket.sendall(packet)

    def close(self) -> None:
        """Close the socket connection."""
        self.run = False
        self.socket.close()
