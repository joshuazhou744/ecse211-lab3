import config
from movement import drive_distance, turn_to
from odometer import Odometer

def main():
    try:
        config.initialize()
        config.stop_motors()

        odom = Odometer(
                config.left_motor,
                config.right_motor,
                config.WHEEL_RADIUS,
                config.TRACK_WIDTH
                )

        drive_distance(config.TILE_SIZE, odom)

        x, y, theta = odom.get_position()
        print(f"Final: x={x:.2f} cm, y={y:.2f} cm, theta={theta:.2f}°")
    finally:
        config.stop_motors()


if __name__ == "__main__":
    main()
