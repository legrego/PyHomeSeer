import pyhomeseer

client = pyhomeseer.HomeSeerClient("192.168.1.20", "guest", "guest")

# Control by Value
pyhomeseer.control(client, ref=123, value=255)

# Control by Label
pyhomeseer.control(client, ref=123, label="On")
