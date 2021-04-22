import cv2
import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter('camera2.avi',fourcc, 30.0, (1920,1080), 1) # Sondaki 0 grayscale kaydedeceğimiz için

def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

width = 1920
height = 1080
bg = np.zeros((height, width, 3), np.uint8)
XPoints = []
YPoints = []
Points = []
Numberofpoints = 50
isInfected = np.zeros((1, Numberofpoints),np.uint8)
InitialInfected = 1
for j in range(InitialInfected):
    isInfected[0][j] = 1
InfectedCounter = InitialInfected
InfectionTimes = []
InfectedList = []
#print(isInfected)
mesafe = 25

movementRate = 5
for i in range(Numberofpoints):
    PointX = random.randint(mesafe, width - mesafe)
    PointY = random.randint(mesafe, height - mesafe)
    XPoints.append(PointX)
    YPoints.append(PointY)
    #cv2.circle(bg, (PointX, PointY), 3, (200, 200, 200), 5)

start_time = time.time()
time_count = 0
cnt = 0
while True:
    frame = bg.copy()
    Points.clear()
    #movementRate += 0.004
    for i in range(Numberofpoints):

        moveleft = random.randint(0, int(movementRate))
        moveup = random.randint(0, int(movementRate))
        movedown = random.randint(0, int(movementRate))
        moveright = random.randint(0, int(movementRate))
        XPoints[i] -= moveleft + int(9*i/(Numberofpoints - i + 1))
        XPoints[i] += moveright + int(9*i/(Numberofpoints - i + 1))
        YPoints[i] -= moveup + int(9*i/(Numberofpoints - i + 1))
        YPoints[i] += movedown + int(9*i/(Numberofpoints - i + 1))

        #Sınırlar
        if XPoints[i] >= width - mesafe : XPoints[i] = width - mesafe
        if XPoints[i] <= mesafe : XPoints[i] = mesafe
        if YPoints[i] >= height - mesafe : YPoints[i] = height - mesafe
        if YPoints[i] <= mesafe : YPoints[i] = mesafe

        Points.append((XPoints[i], YPoints[i]))
        cv2.circle(frame, (XPoints[i], YPoints[i]), 6, (200, 200, 200), 15)
        cv2.putText(frame, str(i+1), (XPoints[i] - 10, YPoints[i]+ 4), cv2.FONT_ITALIC, 0.5, (0, 90, 240), 2)
        if isInfected[0][i] == 0:
            cv2.circle(frame, (XPoints[i], YPoints[i]), mesafe, (0, 200, 0), 2)
        else:
            cv2.circle(frame, (XPoints[i], YPoints[i]), mesafe, (0, 0, 200), 2)


    for i in range(len(Points) ):
        for j in range(len(Points) ):
            #print(Points[i][0], Points[i][1], Points[j][0], Points[j][1])
            if isInfected[0][i] == 1 and isInfected[0][j] == 0:
                dist = calculateDistance(Points[i][0], Points[i][1], Points[j][0], Points[j][1])
                #print(int(dist))
                if dist <= 2* mesafe + 4 and dist != 0:
                    isInfected[0][j] = 1
                    InfectedCounter += 1
                    InfTime = time.time()
                    print(InfectedCounter, "th Infected: ", round((InfTime - start_time), 2))
                    InfectedList.append(InfectedCounter)
                    InfectionTimes.append(InfTime - start_time)


    Totalend = time.time()
    time_count = Totalend - start_time
    cv2.putText(frame, str(round(time_count, 2)), (15, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, "Infected: " + str(InfectedCounter), (1800, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 20, 255), 1)

    cv2.imshow("Korona", frame)
    out.write(frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q") or InfectedCounter == Numberofpoints:
        break

Totalend = time.time()
time_count += Totalend - start_time
print("Total Time: ", time_count)
print("Infection Times: ", InfectionTimes)
print("Infected List: ", InfectedList)
plt.plot(InfectionTimes, InfectedList)
plt.ylabel('Total Infected')
plt.xlabel('Time')
plt.title("Movement Rate: " + str(int(movementRate)) + ",  # of People: " + str(Numberofpoints) + ",  Initial Infected: " + str(InitialInfected))
plt.show()
out.release()
cv2.destroyAllWindows()