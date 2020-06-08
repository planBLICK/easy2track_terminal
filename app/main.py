# -*- coding: utf-8 -*-
# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk, ImageOps
import tkinter as tki
from tkinter import Frame
import threading
import imutils
import cv2
from pyzbar.pyzbar import decode
from time import sleep
import requests
import hashlib
import json
import traceback
from ample import Ample


class Easy2Track:
    def __init__(self, vs, username, password):
        self.ample = Ample()
        self.ample.test().red()

        self.username = username
        self.password = password
        self.apikey = None
        self.perform_login()
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tki.Tk()
        self.root.attributes('-zoomed', True)
        self.root.attributes('-fullscreen', True)
        bg_image = Image.open("/home/pi/easy2track/app/bg.png")
        self.background_image = ImageTk.PhotoImage(bg_image)
        self.bg_label = tki.Label(self.root, image=self.background_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.state = False
        self.root.bind("<F12>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.onClose)
        self.panel = None
        self.success_message = "Vielen Dank, Sie koennen jetzt passieren."
        self.failure_message = "Der Kontakt konnte nicht gespeichert werden, bitte versuchen Sie es erneut."
        self.status = tki.Label(text=self.success_message, font=('Helvetica', 45))
        self.status.place(relx=.5, rely=.5, anchor="center")
        self.status.place_forget()

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        #
        self.root.wm_title("Crowdsoft Easy2Track")
        self.start_fullscreen()

    def perform_login(self):
        request = requests.Session()
        request.auth = (self.username, self.password)
        url = "https://api.planblick.com/login"

        response = request.get(url)
        self.apikey = response.json().get("apikey")


    def is_checked_in(self, data):
        hash = hashlib.md5(data.encode("utf-8")).hexdigest()
        url = "https://api.planblick.com/easy2track/is_checkedin"
        print("HASH", hash)
        payload = json.dumps({"hash": hash})
        headers = {
            'apikey': self.apikey,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        if response.status_code == 200:
            is_checked_in = response.json().get("result")
        else:
            raise Exception("Fehler bei der Überprüfung. Bitte versuchen Sie es erneut. ")

        if is_checked_in is not None:
            print("IS CHECKED IN", is_checked_in)
            return is_checked_in
            pass
        else:
            raise Exception("Fehler bei der Überprüfung. Bitte versuchen Sie es erneut. ")
            pass
        print("RESPONSE", response.text)

    def check_in(self, form_data):
        url = "https://api.planblick.com/es/cmd/addContact"

        payload = json.dumps({
                        "consumer": "demo",
                        "login": "demo_1",
                        "form_data": form_data,
                        "addedtime": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "external_id": ""
                    })
        headers = {
            'apikey': self.apikey,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print("CKECKIN_RESPONSE", response.text)
        if response.status_code==200:
            return True
        else:
            return False

    def check_out(self, form_data):
        url = "https://api.planblick.com/es/cmd/removeContact"

        payload = json.dumps({
                        "consumer": "demo",
                        "login": "demo_1",
                        "form_data": form_data,
                        "deletedtime": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "external_id": ""
                    })
        headers = {
            'apikey': self.apikey,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print("CKECKOUT_RESPONSE", response.text)
        print("CKECKIN_RESPONSE", response.text)
        if response.status_code == 200:
            return True
        else:
            return False

    def start_fullscreen(self, event=None):
        self.state = True  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=600)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = ImageOps.mirror(Image.fromarray(image))

                codes = decode(image)

                if codes is not None and len(codes) > 0:
                    if self.panel is not None:
                        self.panel.place_forget()

                    self.status.place(relx=.5, rely=.5, anchor="center")


                    for code in codes:
                        try:
                            data = json.loads(code.data)
                        except json.decoder.JSONDecodeError:
                            self.status["text"] = "QR-Code ist nicht lesbar oder kein gültiger Kontakt-Code"
                            self.ample.red().blink()
                            print("Not a valid qrcode or not recognized properly")
                            continue

                        if type(data) is not dict:
                            self.status["text"] = "QR-Code ist nicht lesbar oder kein gültiger Kontakt-Code"
                            self.ample.red().blink()
                            print("Not a valid qrcode or not recognized properly")
                            continue
                        data = data.get("data")

                        if not self.is_checked_in(data):
                            print("TRY TO CHECKIN")
                            if self.check_in(data):
                                self.status["text"] = self.success_message
                                self.ample.green().blink(times=5, intervall=1).red()
                            else:
                                self.status["text"] = self.failure_message
                                self.ample.red().blink()
                        else:
                            print("TRY TO CHECKOUT")
                            if self.check_out(data):
                                self.status["text"] = self.success_message
                                self.ample.green().blink(times=5, intervall=1).red()
                            else:
                                self.status["text"] = self.failure_message
                                self.ample.red().blink()

                    sleep(3)

                    self.panel.place(relx=.5, rely=.5, anchor="center")
                    self.status.place_forget()

                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.place(relx=.5, rely=.5, anchor="center")
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
                    self.panel.config(highlightbackground="green")

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.panel.place(relx=.5, rely=.5, anchor="center")
            self.status.place_forget()

    def onClose(self, e=None):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()



# import the necessary packages
from imutils.video import VideoStream
import argparse
import time
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True,
	help="Crowdsoft username")
ap.add_argument("-p", "--password", required=True,
	help="Crodwosft password")
ap.add_argument("-c", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(1.0)
# start the app
pba = Easy2Track(vs, args["username"], args["password"])
pba.root.mainloop()
