class HomeSeerClient:
    def __init__(self, host="127.0.0.1", username="", password=""):
        self.host = host
        self.port = 80
        self.username = username
        self.password=password
        self.protocol = "http"
        self.client_initialized = True
