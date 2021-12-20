import cv2 as cv
import numpy as np

def waste(x):
    pass

def calibrate(frame, boundaries):
    colours = ["Red", "Blue", "Green", "Yellow", "Orange", "White"]
    boundaries = [([132, 137, 117], [179, 255, 255]), 
            ([96, 102, 60], [166, 255, 255]), 
            ([56, 195, 0], [88, 255, 255]), 
            ([25, 96, 179], [160, 211, 226]), 
            ([0, 160, 178], [17, 255, 255]), 
            ([45, 0, 137], [135, 128, 251])]

    # img = cv.resize(frame, (300, 400), interpolation=cv.INTER_AREA)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    img_clone = frame.copy()

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
            result = cv.bitwise_and(frame, frame, mask=mask)
            
            cv.putText(img_clone, "Find " + colours[i], (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv.imshow("Original", img_clone)
            cv.imshow("Mask", mask)
            cv.imshow("Frame Mask", result)
            key = cv.waitKey(1)
            if key == 27:
                break
        
        img_clone = frame.copy()

        boundaries.append((lower.tolist(), upper.tolist()))

        cv.destroyWindow("Original")
        cv.destroyWindow("Mask")
        cv.destroyWindow("Frame Mask")
    
    cv.destroyAllWindows()

    # print("past calibration")
    find_countours(frame, hsv, colours, boundaries)
    return boundaries

#find the actual squares of colour
def find_countours(frame, hsv, colours, boundaries):
    col_count = 0
    for (lower, upper) in boundaries:        
        lower = np.array(lower, dtype='uint8')
        upper = np.array(upper, dtype='uint8')

        mask = cv.inRange(hsv, lower, upper)
        mask = cv.dilate(mask, (20,20))
        # cv.imshow("mask", mask)

        out = cv.bitwise_and(frame, frame, mask=mask)
        # cv.imshow("processed" + str(count), out)
        
        temp = frame.copy()
        contours, hier = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv.contourArea(contour)
            if 500 < area < 6200: 
                x, y, w, h = cv.boundingRect(contour)
                temp = cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)        
                cv.putText(temp, colours[col_count], (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2) 

        col_count += 1
        cv.imshow("cube after", temp)
        cv.waitKey(2000)
    
    print("helloooo")
    cv.destroyAllWindows()
    return
