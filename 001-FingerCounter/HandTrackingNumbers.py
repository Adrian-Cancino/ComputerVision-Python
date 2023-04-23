import cv2
import time
#import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#folderPath = "fingers"
#myList = os.listdir(folderPath)
#print(myList)
#Create a list of images
#overLayList = []

#for imPath in myList:
#    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
#    overLayList.append(image)

#print(overLayList)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)

    if len(lmList) != 0:
        fingers = []

        if (lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]):  # Thumb finger
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5): # 4 Fingers
            if(lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]): #Point number 8 is less then the point number 6
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
        cv2.putText(img, f'Number: {totalFingers}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 0, 0), 3)

    #cv2.putText(img, f'FPS: 1', (100, 70), cv2.FONT_HERSHEY_PLAIN,
    #            3, (255, 0, 0), 3)
    #h, w, c = overLayList[0].shape
    #img[0:h, 0:w] = 1 #Height - Width

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (100, 70), cv2.FONT_HERSHEY_PLAIN,
                2, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)