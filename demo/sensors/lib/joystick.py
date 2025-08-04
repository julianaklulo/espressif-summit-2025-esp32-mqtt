from machine import Pin, ADC


class Joystick:
    """
    A class that represents an analog joystick.

    The joystick has two axis, X and Y, and each axis has a pin
    that it is connected to.
    The joystick has a minimum and maximum threshold for each axis,
    hat will determine the direction that the joystick is being moved to.

    :param pin_x: Pin number for X axis
    :param pin_y: Pin number for Y axis
    :param min: Minimum threshold for the axis
    :param max: Maximum threshold for the axis
    """

    def __init__(self, pin_x, pin_y, min=10000, max=60000):
        self.pin_x = ADC(Pin(pin_x), atten=ADC.ATTN_11DB)
        self.pin_y = ADC(Pin(pin_y), atten=ADC.ATTN_11DB)
        self.min = min
        self.max = max

    def read_x(self) -> int:
        """
        Read the raw analog value from the X axis.
        """
        return self.pin_x.read_u16()

    def read_y(self) -> int:
        """
        Read the raw analog value from the Y axis.
        """
        return self.pin_y.read_u16()

    def get_direction_x(self) -> str:
        """
        Get the direction of the joystick on the X axis.
        """
        if self.read_x() > self.max:
            return "Right"
        elif self.read_x() < self.min:
            return "Left"
        else:
            return "Center"

    def get_direction_y(self) -> str:
        """
        Get the direction of the joystick on the Y axis.
        """
        if self.read_y() > self.max:
            return "Up"
        elif self.read_y() < self.min:
            return "Down"
        else:
            return "Center"

    def get_state(self) -> str:
        """
        Get the state of the joystick in both axis.
        """
        return f"{self.get_direction_x()}:{self.get_direction_y()}"
