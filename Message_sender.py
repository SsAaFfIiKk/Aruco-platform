from paho.mqtt import publish

class SendMessage():
    def __init__(self, hostname):
        self.hostname = hostname

    def crate_msg(self, topic, msg):
        message = [{"topic": topic, "payload": msg}]
        return message

    def send_msg(self,message):
        publish.multiple(message, hostname=str(self.hostname))
