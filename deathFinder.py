import cv2
import numpy as np

def checkContours(contours):
    first = contours[0]
    second = contours[1]

    firstOk = False
    secondOk = False

    for contour in contours:
        max = contour.max()
        min = contour.min()
        size = contour.size

        if max > 1120 and max < 1130 and size > 1400:
            firstOk = True
            continue

        if max > 1070 and max < 1080 and size > 1400:
            secondOk = True

    return firstOk and secondOk

cap = cv2.VideoCapture("./Sekiro1.mp4")

boundaries = [
    ([17, 15, 175], [55, 95, 200])
]

#cap.set(cv2.CAP_PROP_POS_MSEC, 1835000)
#cap.set(cv2.CAP_PROP_POS_MSEC, 1950000)
#cap.set(cv2.CAP_PROP_POS_MSEC, 4712000)
cap.set(cv2.CAP_PROP_POS_MSEC, 7265000)
#cap.set(cv2.CAP_PROP_POS_MSEC, 7517000)

deathStart = False
deaths = 0

frameNum = 0
while True:
    ret, frame = cap.read()
    ret, frame = cap.read()
    
    lower = np.array(boundaries[0][0], dtype="uint8")
    upper = np.array(boundaries[0][1], dtype="uint8")

    mask = cv2.inRange(frame, lower, upper)
    frame_mask = cv2.bitwise_and(frame, frame, mask = mask)
    
    gray_image = cv2.cvtColor(frame_mask, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_image, (7, 7), 0)
    canny2 = cv2.Canny(blurred, 50, 100)
    
    contours, _ = cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print("contours:", len(contours))

    
    if len(contours) >= 2 and len(contours) <= 5 and deathStart == False:
        
        if checkContours(contours):
            deaths += 1
            print("death", deaths)

            #skip 10 seconds for reload
            for i in range(0, 11 * 60):
                ret, frame = cap.read()

    if len(contours) > 0:
        cv2.drawContours(frame, contours, -1, (0,255,0), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Sekiro 1', frame)

    frameNum += 1

cap.release()

cv2.destroyAllWindows()