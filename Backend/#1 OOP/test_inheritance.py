from abc import abstractmethod


class Sender:
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def send(self):
        pass


class SendSMS(Sender):
    def send(self):
        print(self.data)


class SendTELEGRAM(Sender):
    def send(self):
        print(self.data)


sms = SendSMS('fffff')
sms.send()

tg = SendTELEGRAM('gg')
print(tg.data)


class EventUpdate:

    def __init__(self, data):
        self.data = data

    def start(self):
    	return self.data


s = EventUpdate('success').start()

print(s)
