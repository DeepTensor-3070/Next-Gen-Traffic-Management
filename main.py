import cv2
import serial
import time

# Change port if needed
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

cap = cv2.VideoCapture(0)

bg = cv2.createBackgroundSubtractorMOG2()

count = 0
line_y = 300
offset = 10

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640,480))

    fgmask = bg.apply(frame)

    _, thresh = cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame,(0,line_y),(640,line_y),(0,255,0),2)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 2500:

            x,y,w,h = cv2.boundingRect(cnt)
            cx = x + w//2
            cy = y + h//2

            if line_y-offset < cy < line_y+offset:

                count += 1
                print("Cars:",count)

                arduino.write((str(count)+"\n").encode())
                time.sleep(0.5)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.putText(frame,"Cars: "+str(count),(20,50),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow("Vehicle Counter",frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()