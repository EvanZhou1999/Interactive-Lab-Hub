import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model


# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')
# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')

f.close()
print(classNames)

# Initialize the webcam
cap = cv2.VideoCapture(0)

className = ''

while True:
    # Read each frame from the webcam
    _, frame = cap.read()

    y, x, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        handsType = []
        for hand in result.multi_handedness:
            handType=hand.classification[0].label
            handsType.append(handType)
        for handslms in result.multi_hand_landmarks:
            for i, lm in enumerate(handslms.landmark):
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([int(lm.x * y), int(lm.y * x)])
                #cv2.putText(frame, str(i), (lmx-25, lmy+5), cv2.FONT_HERSHEY_SIMPLEX,
                   #0.4, (0,0,255), 2)

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            #prediction = model.predict([landmarks])
            # print(prediction)
            #classID = np.argmax(prediction)
            #className = classNames[classID]
        print(handsType)

    # show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()

