from lib.video import Video
from lib.ui import *
from lib.client import Client
from lib.robot import Robot

window = Window(450*2, 800, "TeleAPP")
left_turn_btn = Button(450+65, 470, 40, 40, (217, 217, 217), window)
right_turn_btn = Button(450+385-40, 470, 40, 40, (217, 217, 217), window)
joystick = Joystick(450+125 + 100, 490 + 100, 100, 20, (217, 217, 217), window)
robot = Robot(window)
user_video = Video(window, crop=(656, 0, 608, 1080))
usb_video = Video(window)
tof_video = Video(window)
client = Client(user_video, usb_video, tof_video, robot, host='192.168.43.161', port=5050)

client.start()
window.start()
user_video.start()

user_video.read()
user_video.get_binary()

while True:
    window.read()
    if not window.run:
        break
    user_video.read()
    joystick.read()
    left_turn_btn.read()
    right_turn_btn.read()

    robot.speed = int(joystick.distance / joystick.r1 * robot.max_speed)
    robot.direction = int(joystick.angle)
    robot.turn_speed = -30 if left_turn_btn.down else 30 if right_turn_btn.down else 0

    window.fill((34, 34, 34))
    joystick.draw()
    left_turn_btn.draw()
    right_turn_btn.draw()
    usb_video.draw(0, 0, 450, 800)
    user_video.draw(341, 610, 89, 170)
    tof_video.draw(450+65, 65, 320, 240)
    window.update()

print('Closing')
client.close()
usb_video.close()
