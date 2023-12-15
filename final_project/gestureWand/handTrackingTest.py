from handtracking import HandTracking

track = HandTracking()

angle = 0

while True:
    detection = track.detectLeftHandAngle()
    if not detection == None:
        angle = detection
    print(angle)