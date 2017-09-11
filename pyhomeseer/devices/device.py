class Device:
    def __init__(self, device_data=None):
        if device_data is None:
            device_data = {}

        self.device_data = device_data

    @property
    def ref(self):
        return self.device_data.get("ref")

    @property
    def name(self):
        return self.device_data.get("name")

    @property
    def location(self):
        return self.device_data.get("location")

    @property
    def location2(self):
        return self.device_data.get("location2")

    @property
    def value(self):
        return self.device_data.get("value")

    @property
    def status(self):
        return self.device_data.get("status")

    def _display_name(self):
        return "{name} ({ref}): {status}".format(
            name=self.name,
            ref=self.ref,
            status=self.status
        )

    def __str__(self):
        return self._display_name()

    def __repr__(self):
        return self._display_name()