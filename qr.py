from pyzbar import pyzbar
import imutils
import time
import cv2
from subprocess import CalledProcessError
cap = cv2.VideoCapture(0)



time.sleep(0.2)
found = set()

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=400)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)

        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        if barcodeData not in found:
            print(barcodeData)
            if(barcodeData=="Drone"):
                print ('Land')

            found.add(barcodeData)

    # show the output frame
    cv2.imshow("QR", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == 27:
        break

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()

