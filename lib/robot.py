"""Provides a class for storing the state of the robot."""


class Robot:
    """Current state of the robot."""

    speed: int = 0
    max_speed: int = 60
    turn_speed: int = 0
    direction: int = 0

    gyro: int = 0
    us: list[int] = [200] * 6
    us_max_dist: int = 200
