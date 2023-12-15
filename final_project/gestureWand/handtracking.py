import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import math
#from tensorflow.keras.models import load_model

class HandTracking():
    def __init__(self):
        # initialize mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils
        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)
    
    def detectStartGesture(self):
        _, frame = self.cap.read()

        y, x, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = self.hands.process(framergb)

        # print(result)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            if len(result.multi_hand_landmarks) < 2:
                return False
            else:
                finger1 = result.multi_hand_landmarks[0].landmark[4] # thumb
                finger2 = result.multi_hand_landmarks[0].landmark[8] # 8 = index finger, 12 for middle
                finger3 = result.multi_hand_landmarks[1].landmark[4] # thumb
                finger4 = result.multi_hand_landmarks[1].landmark[8] # 8 = index finger, 12 for middle
                
                p1 = ((finger1.x + finger2.x)/2, (finger1.y + finger2.y)/2) # middle point of finger1 & 2
                p2 = ((finger3.x + finger4.x)/2, (finger3.y + finger4.y)/2) # middle point of finger3 & 4
                
                threshold = 0.01
                # debug print distance between middle points
                # print(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))
                print(f"{p1[0]-p2[0]}, {p1[1]-p2[1]}")
                if abs(p1[0]-p2[0]) < threshold and abs(p1[1]-p2[1]) < threshold:
                    return True
                else:
                    return False
        
        return False

    def detectThumbCoordinates(self):
        _, frame = self.cap.read()

        y, x, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = self.hands.process(framergb)

        # print(result)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            if len(result.multi_hand_landmarks) < 2:
                return None
            else:
                # we will track thumb only
                finger1 = result.multi_hand_landmarks[0].landmark[4] # thumb
                #finger2 = result.multi_hand_landmarks[0].landmark[8] # 8 = index finger, 12 for middle
                finger3 = result.multi_hand_landmarks[1].landmark[4] # thumb
                #finger4 = result.multi_hand_landmarks[1].landmark[8] # 8 = index finger, 12 for middle
                
                #p1 = ((finger1.x + finger2.x)/2, (finger1.y + finger2.y)/2) # middle point of finger1 & 2
                #p2 = ((finger3.x + finger4.x)/2, (finger3.y + finger4.y)/2) # middle point of finger3 & 4
                
                return ((finger1.x * 1280, finger1.y * 720), (finger3.x * 1280, finger3.y * 720))
                
        return None
    
    def detectThumbAngle(self):  # return 1 for vertical, 2 for horizontal, 3 for 45 degree
        _, frame = self.cap.read()

        y, x, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = self.hands.process(framergb)

        # print(result)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            if len(result.multi_hand_landmarks) < 2:
                return None
            else:
                # we will track thumb only
                finger1 = result.multi_hand_landmarks[0].landmark[4] # thumb
                #finger2 = result.multi_hand_landmarks[0].landmark[8] # 8 = index finger, 12 for middle
                finger3 = result.multi_hand_landmarks[1].landmark[4] # thumb
                #finger4 = result.multi_hand_landmarks[1].landmark[8] # 8 = index finger, 12 for middle
                
                #p1 = ((finger1.x + finger2.x)/2, (finger1.y + finger2.y)/2) # middle point of finger1 & 2
                #p2 = ((finger3.x + finger4.x)/2, (finger3.y + finger4.y)/2) # middle point of finger3 & 4
                
                # check if the coordinates are valid
                if finger1.x == 0 or finger1.y == 0 or finger3.x == 0 or finger3.y == 0:
                    return None
                
                threshold = 0.2
                distance = math.sqrt((finger1.x - finger3.x)**2 + (finger1.y - finger3.y)**2)
                print(distance)
                if distance < threshold:
                    return None
                else:
                    dx = abs(finger1.x - finger3.x)
                    dy = abs(finger1.y - finger3.y)
                    if dy == 0 or dx == 0:
                        return None
                    slope = abs(float(dy) / float(dx))
                    if slope > 3:
                        return 1
                    elif slope < 0.3:
                        return 2
                    else:
                        return 3
                    
                
        return None
                

    
    def detectLeftHandAngle(self):
        _, frame = self.cap.read()

        y, x, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = self.hands.process(framergb)

        # print(result)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            target_hand_id = -1
            for index, hand in enumerate(result.multi_handedness):
                handType=hand.classification[0].label
                if handType == 'Left':
                    target_hand_id = index
                    break
            
            if target_hand_id == -1:
                return None
            else: 
                thumb = result.multi_hand_landmarks[target_hand_id].landmark[4]
                lit_finger = result.multi_hand_landmarks[target_hand_id].landmark[20]
                # print(thumb.y)
                vx = thumb.x - lit_finger.x
                vy = thumb.y - lit_finger.y
                # Calculate the angle in radians
                angle_radians = math.atan2(vy, vx)

                # Convert the angle to degrees
                angle_degrees = math.degrees(angle_radians)

                # Ensure the angle is in the range [0, 360)
                angle_degrees = ((angle_degrees + 360) % 360)
                
                return angle_degrees
        else:
            return None
                
