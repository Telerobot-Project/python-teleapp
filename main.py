from lib.video import Video
from lib.ui import *
from lib.client import Client
from lib.robot import Robot

window = Window(450*3, 700, "TeleAPP")
joystick = Joystick(450*2+225, 509, 100, 20, (217, 217, 217), window)
robot = Robot(window)
user_video = Video(window)
usb_video = Video(window)
tof_video = Video(window)
client = Client(user_video, usb_video, tof_video, robot)

client.start()
window.start()
user_video.start()

while True:
    window.read()
    if not window.run: break
    user_video.read()
    joystick.read()

    robot.speed = int(joystick.distance / joystick.r1 * robot.max_speed)
    robot.direction = int(joystick.angle)

    window.fill((34, 34, 34))
    joystick.draw()
    robot.draw()
    usb_video.draw(450, 0, 450, 700)
    user_video.draw(450+359, 564, 81, 126)
    tof_video.draw(450*2+64, 64, 320, 240)
    window.update()

print('Closing')
client.close()
usb_video.close()