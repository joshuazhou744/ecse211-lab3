import math

class Odometer:
    """x, y position in cm, heading in degrees clockwise from +y axis"""

    def __init__(self, left_motor, right_motor, wheel_radius, track_width):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.wheel_radius = wheel_radius
        self.track_width = track_width

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.prev_left = left_motor.get_position()
        self.prev_right = right_motor.get_position()

    def update(self):
        """Update odometer values"""
        current_left = self.left_motor.get_position()
        current_right = self.right_motor.get_position()
        delta_left = current_left - self.prev_left
        delta_right = current_right - self.prev_right
        self.prev_left = current_left
        self.prev_right = current_right

        d_left = math.radians(delta_left) * self.wheel_radius
        d_right = math.radians(delta_right) * self.wheel_radius

        distance = (d_left + d_right) / 2
        # d_L - d_R = r_L * theta - r_R * theta = (r_L - r_R) * theta
        # right, clockwise turns are positive theta
        delta_theta = (d_left - d_right) / self.track_width

        # use mid theta for average heading to calculate direction/distance traveled
        mid_theta = math.radians(self.theta) + delta_theta / 2
        self.x += distance * math.sin(mid_theta)
        self.y += distance * math.cos(mid_theta)
        self.theta = (self.theta + math.degrees(delta_theta)) % 360

    def correct(self, x=None, y=None, theta=None):
        """Set odometer values to a known position and heading"""
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if theta is not None:
            self.theta = theta % 360

    def get_position(self):
        return (self.x, self.y, self.theta)
