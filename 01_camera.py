import cv2
cap = cv2.VideoCapture(0)


while(1):
    #read the frame
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,1)
        #show the frame
        cv2.imshow('frame',frame)

        k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()




