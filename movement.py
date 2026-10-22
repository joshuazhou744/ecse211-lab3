import config
import time
import math

def drive_distance(cm, odom, timeout=30):
    """Drive foward/backward along current heading"""
    odom.update()
    start_x, start_y, target_heading = odom.get_position()

    heading_rad = math.radians(target_heading)
    direction = 1 if cm >= 0 else -1 # forward or backward
    deadline = time.monotonic() + timeout

    try:
        while True:
            odom.update()
            x, y, heading = odom.get_position()

            progress = (x - start_x) * math.sin(heading_rad) + (y - start_y) * math.cos(heading_rad)
            remaining = abs(cm) - direction * progress

            if remaining <= config.POSITION_TOLERANCE:
                break

            if time.monotonic() >= deadline:
                raise TimeoutError("not completed in time")

            fraction = min(remaining / config.DRIVE_SLOW_DISTANCE, 1.0)
            power = config.DRIVE_MIN_POWER + (config.DRIVE_MAX_POWER - config.DRIVE_MIN_POWER) * fraction
            error = (target_heading - heading + 180) % 360 - 180
            correction = max(-config.MAX_HEADING_CORRECTION, min(config.MAX_HEADING_CORRECTION, config.HEADING_GAIN * error))
            config.left_motor.set_power(direction * power + correction)
            config.right_motor.set_power(direction * power - correction)

            time.sleep(0.01)
    finally:
        config.stop_motors()
        time.sleep(0.1)
        odom.update()

def turn_to(theta, odom, timeout=30):
    """Turn to given theta degrees"""
    odom.update()
    deadline = time.monotonic() + timeout

    try:
        while True:
            odom.update()
            _, _, heading = odom.get_position()

            error = (theta - heading + 180) % 360 - 180
            if abs(error) <= config.ANGLE_TOLERANCE:
                break

            if time.monotonic() >= deadline:
                raise TimeoutError("not completed in time")

            fraction = min(abs(error) / config.TURN_SLOW_ANGLE, 1.0)
            power = config.TURN_MIN_POWER + (config.TURN_MAX_POWER - config.TURN_MIN_POWER) * fraction

            if error > 0: # clockwise
                config.left_motor.set_power(power)
                config.right_motor.set_power(-power)
            else:
                config.left_motor.set_power(-power)
                config.right_motor.set_power(power)

            time.sleep(0.01)
    finally:
        config.stop_motors()
        time.sleep(0.1)
        odom.update()
