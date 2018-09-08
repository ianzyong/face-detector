# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 14:15:31 2018

@author: ianzy
"""

#import numpy as np
import cv2
import math
import time
#import tkinter
#import pdb
import random

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if(ret == False):
    cap = cv2.VideoCapture(0)
width = int(cap.get(3))  # float
height = int(cap.get(4)) # float 
mcounter = 0
it = 0
resettime = 15
starttime = time.clock()

while(cap.isOpened()):
    it+=1
    
    ret, frame = cap.read()
    if ret==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        fcounter = len(faces)
        
        if mcounter < fcounter:
            mcounter = fcounter
        
        if time.clock() - starttime > resettime:
            localtime = time.asctime( time.localtime(time.time()) )
            print('---')
            print('Max face counter reset, max faces = {}'.format(mcounter))
            print('Current time = {}'.format(localtime))
            mcounter = 0
            starttime = time.clock()
            
           
        for (topleft_x,topleft_y,head_width,head_height) in faces:
            center_x = int((2*topleft_x+head_width)/2)
            center_y = int((2*topleft_y+head_height)/2)
            head_radius = (head_width + head_height)/4
            cv2.circle(frame, (center_x,center_y), (int(head_radius)), (255*abs(math.sin(it/20)),head_radius*2,0), 3)#radius must be changed for different computers/different screens
            head_center = (center_x, center_y)
            
#            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
#            for (ex,ey,ew,eh) in eyes:
#                cv2.rectangle((30,50,20),(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
        frame = cv2.flip(frame,1) 
        cv2.rectangle(frame,(10,height-400),(100,height-335),(250,250,250),-1)
        cv2.putText(frame,"faces:",(15,height-370), font, 0.8,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(frame,str(fcounter),(15,height-345), font, 0.8,(0,0,0),2,cv2.LINE_AA)
        
        cv2.rectangle(frame,(10,height-300),(100,height-235),(250,250,250),-1)
        cv2.putText(frame,"max:",(15,height-270), font, 0.8,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(frame,str(mcounter),(15,height-245), font, 0.8,(0,0,0),2,cv2.LINE_AA)
        
        cv2.imshow('frame',frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()