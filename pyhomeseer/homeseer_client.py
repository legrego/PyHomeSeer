""" Client for interacting with a HomeSeer instance """
import requests
from requests.auth import HTTPBasicAuth

from pyhomeseer.error import PyHomeSeerError, PyHomeSeerAuthenticationError
from pyhomeseer.devices.device import Device
from pyhomeseer.devices.controlled_device import ControlledDevice

URL_TEMPLATE = "{protocol}://{host}:{port}/JSON"


class HomeSeerClient:
    """ Client Definition """
    def __init__(self, host="127.0.0.1", username="", password=""):
        """ The HomeSeer Client """

        self.host = host
        self.port = 80
        self.username = username
        self.password = password
        self.protocol = "http"
        self.client_initialized = True

    def get_devices(self, ref=None, location=None, location2=None):
        """ Retrieve all available devices from HomeSeer """

        params = {
            "request": "getstatus",
            "ref": ref,
            "location": location,
            "location2": location2
        }

        devices_request = requests.get(self._build_url(), auth=self._build_auth(), params=params)

        self._check_if_unauthorized(devices_request)

        if devices_request.status_code != 200:
            error_msg = "HomeSeer returned unexpected status code: {code}".format(code=devices_request.status_code)
            raise PyHomeSeerError(error_msg)

        device_json_response = devices_request.json()

        all_devices = list(map(Device, device_json_response.get("Devices")))

        return all_devices

    def get_control(self, ref=None):
        """ Retrieve all available controllable devices from HomeSeer """

        params = {
            "request": "getcontrol",
            "ref": ref
        }

        devices_request = requests.get(self._build_url(), auth=self._build_auth(), params=params)

        self._check_if_unauthorized(devices_request)

        if devices_request.status_code != 200:
            error_msg = "HomeSeer returned unexpected status code: {code}".format(code=devices_request.status_code)
            raise PyHomeSeerError(error_msg)

        device_json_response = devices_request.json()

        all_devices = list(map(ControlledDevice, device_json_response.get("Devices")))

        return all_devices

    def control(self, ref=None, value=None, label=None):
        """ Control the indicated device, either by value or by label """

        if value is not None and label is not None:
            raise PyHomeSeerError(
                "Devices can be controlled by either value or label, but not both. Only set one of these."
            )

        if ref is None:
            raise PyHomeSeerError(
                "Ref is required to control a device."
            )

        post_data = {
            "action": "controlbylabel" if value is None else "controlbyvalue",
            "deviceref": ref,
            "value": value,
            "label": label
        }

        control_device_response = requests.post(self._build_url(), auth=self._build_auth(), json=post_data)

        self._check_if_unauthorized(control_device_response)

        if control_device_response.status_code == 200:
            has_error = control_device_response.text == "error"
            cause = "Unknown HomeSeer Error" if has_error else None

            if not has_error:
                json_response = control_device_response.json()
                response_message = str(json_response.get("Response"))
                if response_message is not None and response_message.find("Error") >= 0:
                    cause = response_message
                    has_error = True

            if has_error:
                raise PyHomeSeerError(
                    "Error controlling device with ref {ref}. Cause: {cause}".format(ref=ref, cause=cause)
                )
        else:
            raise PyHomeSeerError(
                "Error controlling device with ref {ref}. HomeSeer returned unexpected status code: {code}"
                .format(ref=ref, code=control_device_response.status_code)
            )

    @staticmethod
    def _check_if_unauthorized(response):
        if response is not None and response.status_code is not None:
            if response.status_code == 401:
                raise PyHomeSeerAuthenticationError(
                    "Invalid username/password, or user not authorized to perform this action"
                )

    def _build_url(self):
        return URL_TEMPLATE.format(protocol=self.protocol, host=self.host, port=self.port)

    def _build_auth(self):
        auth_required = len(self.username) > 0 and len(self.password) > 0

        auth = None

        if auth_required:
            auth = HTTPBasicAuth(self.username, self.password)

        return auth
