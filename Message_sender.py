from paho.mqtt import publish


class SendMessage():
    def __init__(self):
        self.send_first = False
        self.send_second = False

    def crate_msg(self, topic, msg):
        message = [{"topic": topic, "payload": msg}]
        return message

    def send_first_msg(self, detect_first, message):
        if self.send_first == False and detect_first == True:
            publish.multiple(message, hostname="localhost")
            self.send_first = True

    def send_second_msgs(self, detect_second, message):
        if self.send_second == False and detect_second == True:
            publish.multiple(message, hostname="localhost")
            self.send_second = True
