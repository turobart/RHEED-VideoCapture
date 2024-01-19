import time
import datetime
import tempfile
import os
import sys

import cv2
import numpy as np
from mss import mss
import ast
import serial
from threading import Thread
import math
import json


frame_rate = 24

with open('timeConfig.txt', 'r') as f:
    s = f.read()
    timedata = ast.literal_eval(s)
    
with open('windowConfig.json', 'r') as f:
    screenGrabConfigData = json.load(f)

def setGrabCoordinates(topLeftX, topLeftY, width, height):
    with open('windowConfig.json', 'r+') as f:
        data = json.load(f)

        data['topLeftX'] = topLeftX
        data['topLeftY'] = topLeftY
        data['width'] = width
        data['height'] = height
        
        f.seek(0)
        f.truncate(0)
        json.dump(data, f)
        
def getGrabCoordinates():
    with open('windowConfig.json', 'r+') as f:
        grab_coordinates = json.load(f)
    return grab_coordinates

class PcComm():
    def __init__(self, parent):
        self.IsListening = False
        self.IsCapturing = False
        self.timetext = 0
        self.parent = parent
        

    def StartClicked(self):
            self.IsListening = not self.IsListening
            
            if self.IsListening:
                try:
                    self.ser = serial.Serial('COM4', 9600,
                                        parity=serial.PARITY_EVEN, 
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS,
                                        timeout=1)
                    self.t1 = Thread(target = self.listenToPC)
                    self.t1.setDaemon(True)
                    self.t1.start()
                except:
                    self.IsListening = not self.IsListening
            else:
                self.ser.close()
                self.t1.join()
            return self.IsListening
                
    def listenToPC(self):
        while(self.IsListening):
            if self.ser.in_waiting>0:
                time.sleep(0.5)
                
                self.parent.enableConnect(False)
                self.parent.show_capture_window()
                self.parent.capture_window.record_button.hide()
                self.parent.capture_window.stop_record_button.show()
                self.captureRHEED(self.ser.read().decode())
                self.parent.enableConnect(True)
                self.parent.capture_window.record_button.show()
                self.parent.capture_window.stop_record_button.hide()
                time.sleep(0.5)
                self.ser.reset_input_buffer()
                time.sleep(0.5)
                self.parent.close_capture_window()
                
    def captureRHEED(self, pcTime = None):
        self.parent.set_region_action.setDisabled(True)
        self.IsCapturing = True
        self.custom_name = ''
        exe_path = os.path.normpath('.\\')
        file_out = os.path.join(exe_path, 'temp_video','temp.mp4')
        
#         grab_coordinates = getGrabCoordinates()
        out = cv2.VideoWriter(file_out,
                          cv2.VideoWriter_fourcc(*'mp4v'),
                          frame_rate,
                          (self.parent.capture_window.width, self.parent.capture_window.height),
                          isColor=0)
        bbox = {'top': self.parent.capture_window.top_leftY, 'left': self.parent.capture_window.top_leftX,
                'width': self.parent.capture_window.width, 'height': self.parent.capture_window.height}
#         bbox = {'top': grab_coordinates['topLeftY'], 'left': grab_coordinates['topLeftX'],
#                 'width': grab_coordinates['width'], 'height': grab_coordinates['height']}
        
#         print(out)
#         print(file_out)
        with mss() as sct:
            old_display_time = 0
            run_time = 0
            start = time.time()
            while 'capturing':
                frame_start = time.time()
                im = np.array(sct.grab(bbox))[:,:,2]  # Convert to grayscale
                out.write(im)
                en = time.time()
                
                if pcTime == "A":
                    time_to_run = timedata['short']
                elif pcTime == "B":
                    time_to_run = timedata['medium']
                elif pcTime == "C":
                    time_to_run = timedata['long']
                else:
                    time_to_run = 600
                self.parent.progress.max_value = int(time_to_run)
                
                delay = math.ceil((1 / frame_rate - (en - frame_start)) * 1000) 
                cv2.waitKey(delay)

                if not self.IsCapturing:
                    run_time = time.time() - start
                    self.parent.capture_window.save_video()
                    self.custom_name = self.parent.capture_window.custom_video_name
                    break
                
                if old_display_time < round(run_time):
                    self.timetext = int(time_to_run - math.floor(run_time))
                    self.parent.change_value(math.floor(run_time), self.timetext)
                old_display_time = math.floor(run_time)
                
                run_time = time.time() - start                
                
                if run_time> time_to_run:
                    break
                      
        out.release()
        
        cap = cv2.VideoCapture(file_out)
        ret, frame = cap.read()
    
        
        h, w, _ = frame.shape
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        
        true_fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / run_time
        
        
        
        if self.custom_name == '':
        
            now=datetime.datetime.now()
            
            dd=now.day
            mm=now.month
            yy=now.year
            hh=now.hour
            mins = now.minute
            year_t=str(yy)
            if dd<10: day_t='0'+str(dd)
            else: day_t=str(dd)
            if mm<10: month_t='0'+str(mm)
            else: month_t=str(mm)
            if hh<10: hour_t='0'+str(hh)
            else: hour_t=str(hh)
            if mins<10: mins_t='0'+str(mins)
            else: mins_t=str(mins)
        
            current_date = "%s_%s_%s-%s_%s.mp4" % (year_t, month_t, day_t, str(hour_t), str(mins_t))
            
            video_path = os.path.join(exe_path, 'auto_capture_videos', current_date)
        else:
            video_path = self.custom_name
        
        writer = cv2.VideoWriter(video_path, fourcc, true_fps, (w, h))
        
        while ret:
            writer.write(frame)
            ret, frame = cap.read()
        
        writer.release()
        cap.release()

        self.timetext = 0
        self.parent.change_value(0, self.timetext)
        self.IsCapturing = False
        self.parent.set_region_action.setDisabled(False)
        