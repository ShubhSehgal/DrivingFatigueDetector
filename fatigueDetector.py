import numpy as np
from cv2 import cv2

# INSTRUCTIONS
# 1. Download Python
# 2. Download OpenCV
# 3. Downloaod the following files and add them to the project folder (folder the python script is saved in)
#       LINK:   https://github.com/opencv/opencv/tree/master/data/haarcascades
#       File 1: haarcascade_frontalface_default.xml 
#       File 2: haarcascade_eye_tree_eyeglasses.xml

# 4. Add the path for xml files in the brackets in the code below
#    Example: 
#       'C:\\Users\\username\\Desktop\\projectfolder\\haarcascade_frontalface_default.xml'
#       'C:\\Users\\username\\Desktop\\projectfolder\\haarcascade_eye_tree_eyeglasses.xml'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

cap = cv2.VideoCapture(0) 
cap.set(3,640)
cap.set(4,480)

eyes_closed = True #initialize variable to hold status of eyes
face_detected = False #initialize variable to hold status of whether face is detected
asleep = False #initialize variable to hold status of whether user is asleep

blinks_num = 0 #number of blinks recorded
blink_duration = 0 #duration of blink in frames 
total_blink_duration = 0 #sum off all the blink durations
avg_blink_duration = 0 #average duration of blinks


while(True):
    ret, frame = cap.read()  # Capture frame-by-frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray,1.5,5) #detect faces
    cv2.putText(frame,"Blinks: " + str(blinks_num),(70,400),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1) #display blinks 
    cv2.putText(frame,"Average Blink Duration: " + str(avg_blink_duration),(70,425),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1) #display avg blink duration

    #if there are faces in frame, execute this code
    if(len(faces)>0):
        
        face_detected = True #change status to true

        #blink duration is too long, give warning
        if( (not asleep) and avg_blink_duration >= 10):
            warning = cv2.putText(frame,"Warning! User may be fatigued!",(70,450),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        
        for (x,y,w,h) in faces:
            print(x,y,w,h)
            user_face = cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2) 
            roi = gray[y:y+h,x:x+w]
            roi_color = user_face[y:y+h,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi,1.3,5) #detect eyes

            #if eyes are detected
            if(len(eyes)>=2):
                
                #calculate updated avg blink duration
                if(blinks_num >= 1):
                    total_blink_duration += blink_duration
                    avg_blink_duration = total_blink_duration/blinks_num 

                eyes_closed = False #change status
                asleep = False #change status
                blink_duration = 0 #reset blink duration

                status = cv2.putText(frame,"Eyes open",(70,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)
                
                for (xE,yE,wE,hE) in eyes:
                    user_eyes = cv2.rectangle(roi_color, (xE,yE),(xE+wE,yE+hE),(255,255,255),2) #place box around eyes
            
            #eyes not detected
            else:
                #if eyes were previously open and now they're closed, register as blink 
                if( (not eyes_closed) and face_detected):
                    status = cv2.putText(frame,"Blink Detected", (70,70),cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),2) 
                    blinks_num += 1
                    eyes_closed = True

                #program may have just begun, so eyes many have not been detected, do not register as blink
                elif(blinks_num == 0):
                    status = cv2.putText(frame,"No eyes detected", (70,70),cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2) 

                #if face is detected, eyes are closed, and the program has been running, increase the blink duration
                elif(face_detected):
                    blink_duration += 1
                    #if user's eyes are closed for more than 100 frames, he/she may be asleep
                    if (blink_duration >= 200):
                        asleep = True
                        warning = cv2.putText(frame,"Warning! User may be asleep!",(70,450),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
    
    #tell user no face was detected
    else: 
        status = cv2.putText(frame,"No face detected",(70,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2)
        face_detected = False
            

    # Display the frame
    cv2.imshow('frame',frame)
    a = cv2.waitKey(10) 
    if a==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()