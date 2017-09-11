from .device import Device


class ControlledDevice(Device):

    def __init__(self, device_data=None, control_data=None):
        super(ControlledDevice, self).__init__(device_data)
        self.controlData=control_data
