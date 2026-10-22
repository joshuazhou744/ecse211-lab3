import math
import time
import config
from movement import drive_distance, turn_to

def travel_to(x_tile, y_tile, odom, timeout=60):
    """Travel directly, short path"""
    target_x = x_tile * config.TILE_SIZE
    target_y = y_tile * config.TILE_SIZE

    odom.update()
    x, y, _ = odom.get_position()
    dx = target_x - x
    dy = target_y - y
    distance = math.hypot(dx, dy)

    if distance <= config.POSITION_TOLERANCE:
        return

    heading = math.degrees(math.atan2(dx, dy))
    turn_to(heading, odom)
    odom.print_position()
    deadline = time.monotonic() + timeout

    try:
        while True:
            odom.update()
            odom.print_position()
            x, y, heading = odom.get_position()

            dx = target_x - x
            dy = target_y - y
            remaining = math.hypot(dx, dy)

            if remaining <= config.POSITION_TOLERANCE:
                break
            if time.monotonic() >= deadline:
                raise TimeoutError("not reached in time")

            target_heading = math.degrees(math.atan2(dx, dy))
            error = (target_heading - heading + 180) % 360 - 180

            if abs(error) > 30: # badly misaligned
                config.stop_motors()
                turn_to(
                    target_heading,
                    odom,
                    timeout=max(0.01, deadline - time.monotonic()),
                )
                continue

            fraction = min(remaining / config.DRIVE_SLOW_DISTANCE, 1.0)
            power = (
                config.DRIVE_MIN_POWER + (config.DRIVE_MAX_POWER - config.DRIVE_MIN_POWER) * fraction
            )
            correction = max(
                    -config.MAX_HEADING_CORRECTION,
                    min(
                        config.MAX_HEADING_CORRECTION,
                        config.HEADING_GAIN * error
                    )
            )
            config.left_motor.set_power(power + correction)
            config.right_motor.set_power((power - correction) * config.RIGHT_POWER_SCALE)
            time.sleep(0.01)
    finally:
        config.stop_motors()
        time.sleep(0.1)
        odom.update()

def navigate_shortest(waypoints, odom):
    for x_tile, y_tile in waypoints:
        travel_to(x_tile, y_tile, odom)
