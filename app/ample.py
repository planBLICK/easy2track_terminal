import RPi.GPIO as GPIO
from time import sleep


class Ample:

    def __init__(self):
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        self._red = {"pin": 21, "status": True}
        self._yellow = {"pin": 16, "status": False}
        self._green = {"pin": 20, "status": False}
        GPIO.setup(self._red.get("pin"), GPIO.OUT)
        GPIO.setup(self._yellow.get("pin"), GPIO.OUT)
        GPIO.setup(self._green.get("pin"), GPIO.OUT)
        self.update()

    def __del__(self):
        GPIO.cleanup()

    def test(self):
        self.all_on()
        sleep(1)
        self.red()
        sleep(1)
        self.yellow()
        sleep(1)
        self.green()
        sleep(1)
        self.all_off()
        sleep(0.2)
        self.all_on()
        sleep(0.2)
        self.all_off()
        sleep(0.2)
        self.all_on()
        sleep(0.2)
        self.all_off()
        sleep(0.2)
        self.all_on()
        sleep(0.2)
        self.all_off()
        return self

    def all_on(self):
        GPIO.output(self._red.get("pin"), GPIO.HIGH)
        GPIO.output(self._yellow.get("pin"), GPIO.HIGH)
        GPIO.output(self._green.get("pin"), GPIO.HIGH)
        self.update()
        return self

    def all_off(self):
        GPIO.output(self._red.get("pin"), GPIO.LOW)
        GPIO.output(self._yellow.get("pin"), GPIO.LOW)
        GPIO.output(self._green.get("pin"), GPIO.LOW)
        return self

    def update(self):
        GPIO.output(self._red.get("pin"), GPIO.HIGH if self._red.get("status") else GPIO.LOW)
        GPIO.output(self._yellow.get("pin"), GPIO.HIGH if self._yellow.get("status") else GPIO.LOW)
        GPIO.output(self._green.get("pin"), GPIO.HIGH if self._green.get("status") else GPIO.LOW)
        return self

    def red(self):
        self._red["status"] = True
        self._yellow["status"] = False
        self._green["status"] = False
        self.update()
        return self

    def yellow(self):
        self._red["status"] = False
        self._yellow["status"] = True
        self._green["status"] = False
        self.update()
        return self

    def green(self):
        self._red["status"] = False
        self._yellow["status"] = False
        self._green["status"] = True
        self.update()
        return self

    def blink(self, times=3, intervall=0.6):
        for i in range(0, times):
            sleep(0.1)
            self.all_off()
            sleep(intervall/2)
            self.update()
            sleep(intervall/2)
        return self


