from os import system as exec_cmd
from time import sleep
import RPi.GPIO as GPIO


class HomeGuardian:
    """ 
        Home security app using Raspberry PI with motion detector sensor
        and Android phone connected (for taking pictures).
    """

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.pins = {
            "motion_detector": 2,
            "LED": 12,
            "speaker": 14
        }

        self.adb_commands = {
            "screen": "adb shell input keyevent 26",  # turn ON/OFF phone screen
            "camera": "adb shell input keyevent 27",  # open camera app
            "vol_up": "adb shell input keyevent 24",  # volume UP (used to take picture)
            "back": "adb shell input keyevent 4"      # press 'back' button to exit app
        }

        GPIO.setup(self.pins['motion_detector'], GPIO.IN)
        GPIO.setup(self.pins['speaker'], GPIO.OUT)
        GPIO.setup(self.pins['LED'], GPIO.OUT)
        print("Motion detector system is working...")


    def motion_detection(self):
        if GPIO.input(self.pins['motion_detector']) == 1:
            print("Motion detected!")
            self.set_pin_state("speaker", "ON")
            self.set_pin_state("LED", "ON")
            sleep(0.2)
            self.take_picture()
            self.set_pin_state("speaker", "OFF")
            sleep(1)
            self.set_pin_state("LED", "OFF")
        sleep(5)


    def take_picture(self):
        """ Taking picture with phone using 'adb' commands. """
        print("Taking picture...")
        exec_cmd(self.adb_commands["screen"])
        sleep(0.5)
        exec_cmd(self.adb_commands["camera"])
        sleep(1)
        exec_cmd(self.adb_commands["vol_up"])
        sleep(0.5)
        exec_cmd(self.adb_commands["back"])
        exec_cmd(self.adb_commands["screen"])
        print("Picture ready.")


    def set_pin_state(self, device, state):
        """ Turning ON/OFF devices connected to the raspberry. """
        state = 0 if state == "OFF" else 1
        GPIO.output(self.pins[device], state)


    def download_picture_from_phone(self):
        """ Save picture from phone to raspberry to send it via email. """
        pass


    def send_email_alert(self):
        """ Send email/sms alert when motion detected. """
        pass


    def __del__(self):
        self.set_pin_state("LED", "OFF")
        self.set_pin_state("speaker", "OFF")
        print("Motion detector system stopped.")


if __name__ == "__main__":

    pi = HomeGuardian()

    while True:
        pi.motion_detection()
