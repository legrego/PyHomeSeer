"""
PyHomeSeer: interact with your HomeSeer service
"""
from __future__ import print_function

import sys

# pylint: disable=wildcard-import
import requests
from requests.auth import HTTPBasicAuth

from pyhomeseer.devices.device import Device
from pyhomeseer.devices.controlled_device import ControlledDevice

from .error import (
    PyHomeSeerError,
    PyHomeSeerAuthenticationError
)
from .homeseer_client import (
    HomeSeerClient
)

# For Python 2.x we need to decode __repr__ Unicode return values to str
NON_UNICODE_REPR = sys.version_info < (3, )

URL_TEMPLATE = "{protocol}://{host}:{port}/JSON"


def get_devices(client, ref=None, location=None, location2=None):
    """ Retrieve all available devices from HomeSeer """

    _check_client(client)

    params = {
        "request": "getstatus",
        "ref": ref,
        "location": location,
        "location2": location2
    }

    devices_request = requests.get(_build_url(client), auth=_build_auth(client), params=params)

    _check_if_unauthorized(devices_request)

    if devices_request.status_code != 200:
        error_msg = "HomeSeer returned unexpected status code: {code}".format(code=devices_request.status_code)
        raise PyHomeSeerError(error_msg)

    device_json_response = devices_request.json()

    all_devices = list(map(Device, device_json_response.get("Devices")))

    return all_devices


def get_control(client, ref=None):
    """ Retrieve all available controllable devices from HomeSeer """

    _check_client(client)

    params = {
        "request": "getcontrol",
        "ref": ref
    }

    devices_request = requests.get(_build_url(client), auth=_build_auth(client), params=params)

    _check_if_unauthorized(devices_request)

    if devices_request.status_code != 200:
        error_msg = "HomeSeer returned unexpected status code: {code}".format(code=devices_request.status_code)
        raise PyHomeSeerError(error_msg)

    device_json_response = devices_request.json()

    all_devices = list(map(ControlledDevice, device_json_response.get("Devices")))

    return all_devices


def control(client, ref=None, value=None, label=None):
    _check_client(client)

    if value != None and label != None:
        raise PyHomeSeerError(
            "Devices can be controlled by either value or label, but not both. Only set one of these."
        )

    if ref is None:
        raise PyHomeSeerError(
            "Ref is required to control a device."
        )

    postData = {
        "action": "controlbylabel" if value is None else "controlbyvalue",
        "deviceref": ref,
        "value": value,
        "label": label
    }

    control_device_response = requests.post(_build_url(client), auth=_build_auth(client), json=postData)

    _check_if_unauthorized(control_device_response)

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
        raise PyHomeSeerError (
            "Error controlling device with ref {ref}. HomeSeer returned unexpected status code: {code}"
                .format(ref=ref, code=control_device_response.status_code)
        )


def _check_client(client):
    if client is None or not client.client_initialized :
        raise PyHomeSeerError("Initialized Client must be provided")


def _check_if_unauthorized(response):
    if response is not None and response.status_code is not None:
        if response.status_code == 401:
            raise PyHomeSeerAuthenticationError(
                "Invalid username/password, or user not authorized to perform this action"
            )

def _build_url(client):
    return URL_TEMPLATE.format(protocol=client.protocol, host=client.host, port=client.port)


def _build_auth(client):
    auth_required = len(client.username) > 0 and len(client.password) > 0

    auth = None

    if auth_required:
        auth = HTTPBasicAuth(client.username, client.password)

    return auth