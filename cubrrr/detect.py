import requests
import cv2 as cv
import numpy as np
import imutils
  
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

def calibrate(img):
    colours = ["Red", "Blue", "Green", "Yellow", "Orange", "White"]
    boundaries = []
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    img_clone = img.copy()

    window_name = "HSV Value" 
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)

    cv.createTrackbar("H MIN", "HSV Value", 0, 179, waste)
    cv.createTrackbar("S MIN", "HSV Value", 0, 255, waste)
    cv.createTrackbar("V MIN", "HSV Value", 0, 255, waste)
    cv.createTrackbar("H MAX", "HSV Value", 179, 179, waste)
    cv.createTrackbar("S MAX", "HSV Value", 255, 255, waste)
    cv.createTrackbar("V MAX", "HSV Value", 255, 255, waste)

    for i in range(6):
        while True:
            h_min = cv.getTrackbarPos("H MIN", "HSV Value")
            s_min = cv.getTrackbarPos("S MIN", "HSV Value")
            v_min = cv.getTrackbarPos("V MIN", "HSV Value")
            h_max = cv.getTrackbarPos("H MAX", "HSV Value")
            s_max = cv.getTrackbarPos("S MAX", "HSV Value")
            v_max = cv.getTrackbarPos("V MAX", "HSV Value")

            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])

            mask = cv.inRange(hsv, lower, upper)
            result = cv.bitwise_and(img, img, mask=mask)
            
            cv.putText(img_clone, "Find " + colours[i], (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv.imshow("Original", img_clone)
            cv.imshow("Mask", mask)
            cv.imshow("Frame Mask", result)
            key = cv.waitKey(1)
            if key == 27:
                break
        
        img_clone = img.copy()

        boundaries.append((lower.tolist(), upper.tolist()))

        cv.destroyWindow("Original")
        cv.destroyWindow("Mask")
        cv.destroyWindow("Frame Mask")
    
    print(boundaries)

    # count = 1  
    # for (lower, upper) in boundaries:
    #     # (lower, upper) = boundaries[4]
            
    #     lower = np.array(lower, dtype='uint8')
    #     upper = np.array(upper, dtype='uint8')

    #     mask = cv.inRange(hsv, lower, upper)
    #     mask = cv.dilate(mask, (20,20))
    #     # cv.imshow("mask", mask)

    #     out = cv.bitwise_and(img, img, mask=mask)
    #     cv.imshow("processed" , out)
        
    #     temp = img.copy()
    #     contours, hier = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #     for pic, contour in enumerate(contours):
    #         area = cv.contourArea(contour)
    #         if 500 < area < 6200: 
    #             x, y, w, h = cv.boundingRect(contour)
    #             temp = cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
    #             cv.putText(temp, "a", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255)) 

    #     cv.imshow("cube after" , temp)
    #     count+= 1

if __name__ == "__main__":    
    user = input("Do you want to calibrate? ")
    calib_done = False
    
    if user.lower() == "y":
        print("calibrating")
        while not calib_done:
            print("Calibrate with this image? Y/N")
            frame = get_frame()

            cv.imshow("Sample Image", frame)
            key = cv.waitKey(0) & 0xFF
            if key == ord("y"):
                print("! THIS IS THE ONE !")
                calib_done = True
            else: 
                print("andddd we go again.")
            cv.destroyWindow("Sample Image")


        print("Press any key to continue")
        cv.imshow("final image", frame)
        cv.waitKey(0)
        cv.destroyWindow("final image")

        calibrate(frame)

    show_cam()





    cv.destroyAllWindows()

