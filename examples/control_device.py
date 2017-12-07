from pyhomeseer.homeseer_client import HomeSeerClient

client = HomeSeerClient("192.168.1.20", "guest", "guest")

# Control by Value
client.control(ref=123, value=255)

# Control by Label
client.control(ref=123, label="On")
