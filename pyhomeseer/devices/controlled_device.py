""" Represents a Controllable Device within HomeSeer """
from .device import Device


class ControlledDevice(Device):
    """ A Controllable Device """

    def __init__(self, device_data=None, control_data=None):
        """ Constructor """
        super(ControlledDevice, self).__init__(device_data)
        self.control_data = control_data
