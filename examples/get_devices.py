from pyhomeseer.homeseer_client import HomeSeerClient

client = HomeSeerClient("192.168.1.20", "guest", "guest")

all_devices = client.get_devices()

for device in all_devices:
    print(
        "ref={ref}, name={name}, location={location}, value={value}, status={status}".format(
            ref=device.ref,
            name=device.name,
            location=device.location,
            value=device.value,
            status=device.status
        )
    )

device_by_ref = client.get_devices(ref=123)

devices_by_location = client.get_devices(location="First Floor")
