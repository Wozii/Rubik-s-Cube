import requests
import cv2 as cv
import numpy as np
import imutils

from calibrate import calibrate

url = "http://192.168.0.159:8080/shot.jpg"

boundaries = [([0, 180, 97], [6, 255, 255]), 
            ([79, 69, 16], [179, 255, 255]), 
            ([44, 131, 81], [87, 255, 255]), 
            ([17, 120, 123], [31, 255, 255]), 
            ([0, 183, 149], [17, 255, 255]), 
            ([0, 0, 150], [22, 99, 185])] 

def show_cam():
    lower = np.array((0, 0, 0), dtype='uint8')
    upper = np.array((255, 255, 255), dtype='uint8')
    while True:
        frame = get_frame()

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        mask = cv.inRange(hsv, lower, upper)
        mask = cv.dilate(mask, (20, 20))

        out = cv.bitwise_and(frame, frame, mask=mask)

        cv.imshow("Android_cam", out)
        cv.imshow("Mask", mask)

        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord('r'):
            print("red")
            lower, upper = get_boundaries(0)
        elif key == ord('b'):
            print("blue")
            lower, upper = get_boundaries(1)
        elif key == ord('g'):
            print("green")
            lower, upper = get_boundaries(2)
        elif key == ord('y'):
            print("yellow")
            lower, upper = get_boundaries(3)
        elif key == ord('o'):
            print("orange")
            lower, upper = get_boundaries(4)
        elif key == ord('w'):
            print("white")
            lower, upper = get_boundaries(5)
        elif key == ord('n'):
            print("none")
            lower, upper = np.array((0, 0, 0), dtype='uint8'), np.array((255, 255, 255), dtype='uint8')

def get_boundaries(index):
    (lower, upper) = boundaries[index]
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')
    
    return lower, upper
    
def get_frame():
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)
    return img

def waste(x):
    pass


if __name__ == "__main__":    
    user = input("Do you want to calibrate? ")
    calib_done = False
    
    if user.lower() == "y":
        # print("calibrating")
        while not calib_done:
            print("Calibrate with this image? Y/N")
            frame = get_frame()

            cv.imshow("Sample Image", frame)
            key = cv.waitKey(0) & 0xFF
            if key == ord("y"):
                # print("! THIS IS THE ONE !")
                calib_done = True
            else: 
                print("andddd we go again.")
            cv.destroyWindow("Sample Image")


        # print("Press any key to continue")
        # cv.imshow("final image", frame)
        # cv.waitKey(0)
        # cv.destroyWindow("final image")

        boundaries = calibrate(frame, boundaries)

    show_cam()

    cv.destroyAllWindows()

