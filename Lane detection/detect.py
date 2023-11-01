import cv2
import numpy as np
import utlis
import serial
import pygame
import time

curveList = []
avgVal=10

timeT=1

'''pygame.init()
win = pygame.display.set_mode((100,100))'''

def getLaneCurve(img,display=2):

    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utlis.thresholding(img)

    #### STEP 2
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)

    #### STEP 3
    middlePoint,imgHist = utlis.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    #### STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)

    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1

    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4,240)
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    
    
    intialTrackBarVals = [59, 156, 0, 240 ]
    utlis.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        '''
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        '''
        
        '''for eve in pygame.event.get():pass
        keyInput = pygame.key.get_pressed()
        '''

        success, img = cap.read()
        #img = cv2.resize(img,(480,240))
        curve = getLaneCurve(img,display=2)
        print(curve)
        '''if keyInput [pygame.K_q]:'''
        if curve < -0.05:
            ser.write("l".encode('utf-8'))
        elif curve > 0.05:
            ser.write("r".encode('utf-8'))
        else:
            ser.write("f".encode('utf-8'))
        '''
        elif keyInput [pygame.K_x]:     #reverse
            ser.write("R".encode('utf-8'))
        elif keyInput [pygame.K_a]:     #left
            ser.write("l".encode('utf-8'))
        elif keyInput [pygame.K_d]:     #right
            ser.write("r".encode('utf-8'))
        elif keyInput [pygame.K_w]:     #forward
            ser.write("f".encode('utf-8'))
        elif keyInput [pygame.K_s]:     #stop
            ser.write("x".encode('utf-8'))
        
        #for turning on or off the sonar sensor
        elif keyInput [pygame.K_0]:
            ser.write("0".encode('utf-8'))
        elif keyInput [pygame.K_1]:
            ser.write("1".encode('utf-8'))
        '''
        timeT += 1
        if timeT % 10 ==0:
            ser.write("x".encode('utf-8'))
        cv2.imshow('Vid',img)
        cv2.waitKey(1)
