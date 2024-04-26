"""Client application for remotely controlling the robot."""

from lib.client import Client, ConnectionInfo, RobotVideo
from lib.robot import Robot
from lib.ui import Button, Joystick, JoysticSize, Point, Rectangle, Window
from lib.video import UserVideo, Video

window = Window(450 * 2, 800, "TeleAPP")
left_turn_btn = Button(
    Rectangle(x=450 + 65, y=470, width=40, height=40),
    (217, 217, 217),
    window,
)
right_turn_btn = Button(
    Rectangle(x=450 + 385 - 40, y=470, width=40, height=40),
    (217, 217, 217),
    window,
)
joystick = Joystick(
    Point(450 + 125 + 100, 490 + 100),
    JoysticSize(100, 20),
    (217, 217, 217),
    window,
)
robot = Robot()
user_video = UserVideo(window)
usb_video = Video(window)
tof_video = Video(window)
client = Client(
    user_video,
    RobotVideo(usb_video, tof_video),
    robot,
    ConnectionInfo("192.168.43.161", 5050),
)

user_video.read()
user_video.pack()

while True:
    window.read()
    if not window.run:
        break
    user_video.read()
    joystick.read()
    left_turn_btn.read()
    right_turn_btn.read()

    robot.speed = int(joystick.distance / joystick.inner_radius * robot.max_speed)
    robot.direction = int(joystick.angle)
    robot.turn_speed = -30 if left_turn_btn.down else 30 if right_turn_btn.down else 0

    window.fill((34, 34, 34))
    joystick.draw()
    left_turn_btn.draw()
    right_turn_btn.draw()
    usb_video.draw(Rectangle(x=0, y=0, width=450, height=800))
    user_video.draw(Rectangle(x=341, y=610, width=89, height=170))
    tof_video.draw(Rectangle(x=450 + 65, y=65, width=320, height=240))
    window.update()

client.close()
user_video.close()
