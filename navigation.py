import math
import time
import config
from movement import drive_distance, turn_to

def travel_to(x_tile, y_tile, odom):
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
    drive_distance(distance, odom)

def navigate_shortest(waypoints, odom):
    for x_tile, y_tile in waypoints:
        travel_to(x_tile, y_tile, odom)
