# Initialize hardware
from utils.brick import Motor, wait_ready_sensors, EV3ColorSensor, NXTColorSensor

# motors and sensors
left_motor = Motor('C')
right_motor = Motor('B')
left_sensor = EV3ColorSensor(4)
right_sensor = NXTColorSensor(3)

# constants (cm)
WHEEL_RADIUS = 2.08
TRACK_WIDTH = 10.0
SENSOR_OFFSET = 5.0
TILE_SIZE = 30.48

# motor settings
# LEFT_TRIM  = 1.03
# DRIVE_SPEED = 100
# TURN_SPEED = 80
# ALIGN_SPEED = 30

# sensor settings
LEFT_LINE_THRESHOLD = 150
RIGHT_LINE_THRESHOLD = 590

# drive distance
DRIVE_MAX_POWER = 20
DRIVE_MIN_POWER = 12
HEADING_GAIN = 0.5
MAX_HEADING_CORRECTION = 6
DRIVE_SLOW_DISTANCE = 10.0
POSITION_TOLERANCE = 0.5

# turn to
TURN_MAX_POWER = 18
TURN_MIN_POWER = 10
TURN_SLOW_ANGLE = 30.0  # start slowing within 30° of target
ANGLE_TOLERANCE = 2.0  # acceptable heading error in degrees

def initialize():
    wait_ready_sensors(True)

def stop_motors():
    left_motor.set_power(0)
    right_motor.set_power(0)
