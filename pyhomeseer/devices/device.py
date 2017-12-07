""" Represents a Device within HomeSeer """


class Device:
    """ Represents a Device within HomeSeer """
    def __init__(self, device_data=None):
        """ A HomeSeer Device """
        if device_data is None:
            device_data = {}

        self.device_data = device_data

    @property
    def ref(self):
        """ The Device's ref value """
        return self.device_data.get("ref")

    @property
    def name(self):
        """ The Device's name """
        return self.device_data.get("name")

    @property
    def location(self):
        """ The Device's primary location """
        return self.device_data.get("location")

    @property
    def location2(self):
        """ The Device's secondary location"""
        return self.device_data.get("location2")

    @property
    def value(self):
        """ The Device's value """
        return self.device_data.get("value")

    @property
    def status(self):
        """ The Device's status """
        return self.device_data.get("status")

    def _display_name(self):
        """ The Device's Display Name """
        return "{name} ({ref}): {status}".format(
            name=self.name,
            ref=self.ref,
            status=self.status
        )

    def __str__(self):
        return self._display_name()

    def __repr__(self):
        return self._display_name()
