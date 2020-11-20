# DrivingFatigueDetector

Project created using Python and OpenCV with the intended application of monitoring a driver in a car. If the driver falls asleep or exhibits symptoms of fatigue, the program will give a warning. An application like this could be incorporated into vehicles as a safety feature. If the driver falls asleep, the car could give an audio warning, or make the decision to automatically pull over and stop the car (given the car has some autonomous driving features). 

How it works:
DrivingFatigueDetector uses OpenCV to recognize the user's face and eyes. If the user blinks, the program will increment the blink counter and track the duration of each blink. If the average blink duration exceeds a certain amount, the program will conclude that the driver may be drowsy and gives a warning. If the eyes stay completely shut for an extended period, the program will instead send a warning that the driver may be asleep. 

A blink is determined if the user's eyes were previously detected by the program but are not anymore. For each frame of the camera feed in which the eyes remain closed, it increases the counter for the blink duration. If the eyes remain closed for over 200 frames, the program will send a sleep warning. If the average blink duration exceeds 10 frames, then the program will send a fatigue warning.

There may be cases where the program cannot detect the user’s face, and therefore will also fail to detect the eyes. To prevent such a scenario creating a false positive for a blink, a blink will only be registered if the face is detected.

Limitations:
The biggest limitation of this program is its inability to detect a face or facial features under certain conditions. For example, testing the application revealed that the program struggled to consistently detect the eyes for users wearing glasses. 
