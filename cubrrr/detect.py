import cv2 as cv
import numpy as np

def waste(x):
    pass
    
def calibrate(frame):
    colours = ["Red", "Blue", "Green", "Yellow", "Orange", "White"]
    boundaries = []

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
    return boundaries

#find the actual squares of colour
def detect_cube_face(frame, boundaries):
    sq_col = {}
    sq_wh = {}

    # Find the initial contours, show them on the screen
    colours = ["Red", "Blue", "Green", "Yellow", "Orange", "White"]
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
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
            if 500 < area: #6200 
                x, y, w, h = cv.boundingRect(contour)
                temp = cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)        
                cv.putText(temp, colours[col_count], (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2) 

                sq_col[(x, y)] = colours[col_count]
                sq_wh[(x, y)] = (w, h)

        col_count += 1
        cv.imshow("cube after", temp)
        cv.waitKey(2000)
        
    cv.destroyAllWindows()

    # Take the contour information and sort it into 2D array
    # width height of a square; default to high number 
    w_h = [20000, 20000]

    # create 2D array filled with high number tuples by default
    xy = [[(20000, 20000)]*3 for i in range(3)]
    col = [["-"]*3 for i in range(3)]

    # create list of keys and then sort by y value in increasing order
    xy_keys = [*sq_col]
    xy_keys = sorted(xy_keys, key=lambda x: [x[1], x[0]])

    # insert into 2D list and sort by x value, and find the smallest width height of a square
    temp_index = 0
    for i in range(3):
        for j in range(3):
            xy[i][j] = xy_keys[temp_index]

            #set w_h to lowest width height possible
            w_h[0] = sq_wh[xy_keys[temp_index]][0] if sq_wh[xy_keys[temp_index]][0] < w_h[0] else w_h[0]
            w_h[1] = sq_wh[xy_keys[temp_index]][1] if sq_wh[xy_keys[temp_index]][1] < w_h[1] else w_h[1]

            if temp_index < len(xy_keys)-1:
                temp_index += 1
            else: 
                break
        # sort by x
        xy[i] = sorted(xy[i], key=lambda x: [x[0], x[1]])
        
        # create the sorted 2D colour array
        for j in range(3):
            col[i][j] = sq_col[xy[i][j]] if xy[i][j] != (20000, 20000) else "-"
    
    return col
