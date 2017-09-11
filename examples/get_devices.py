import pyhomeseer

client = pyhomeseer.HomeSeerClient("192.168.1.20", "guest", "guest")

all_devices = pyhomeseer.get_devices(client)

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

device_by_ref = pyhomeseer.get_devices(client, ref=123)

devices_by_location = pyhomeseer.get_devices(client, location="First Floor")