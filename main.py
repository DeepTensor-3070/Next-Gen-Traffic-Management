import cv2
import serial
import time

arduino = serial.Serial('/dev/ttyACM0',9600)
time.sleep(2)

cap = cv2.VideoCapture(0)

bg = cv2.createBackgroundSubtractorMOG2()

cars = 0

entry_line = 250
exit_line = 350
offset = 10

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame,(640,480))

    fgmask = bg.apply(frame)

    _, thresh = cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame,(0,entry_line),(640,entry_line),(0,255,0),2)
    cv2.line(frame,(0,exit_line),(640,exit_line),(0,0,255),2)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 2500:

            x,y,w,h = cv2.boundingRect(cnt)

            cx = x + w//2
            cy = y + h//2

            # Entry detection
            if entry_line-offset < cy < entry_line+offset:
                cars += 1
                print("Cars on road:",cars)

            # Exit detection
            if exit_line-offset < cy < exit_line+offset:
                cars -= 1
                if cars < 0:
                    cars = 0
                print("Cars on road:",cars)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.putText(frame,"Cars on Road: "+str(cars),(20,50),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    arduino.write((str(cars)+"\n").encode())

    cv2.imshow("Traffic Monitor",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()