import cv2 as cv
import numpy as np
from detect_face import find_squares

def waste(x):
    pass

def calibrate(img_name, boundaries):
    colours = ["Red", "Blue", "Green", "Yellow", "Orange", "White"]

    face = {}
    face_wh ={}

    cube = cv.imread(img_name)
    img = cv.resize(cube, (300, 400), interpolation=cv.INTER_AREA)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    img_clone = img.copy()

    user = input("Do you want to calibrate the HSV colour channels: Y/N")

    if user.lower() == "y":
        boundaries = []
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

        print("Here are the boundaries:")
        print(boundaries)

    #find the actual squares of colour
    col_count = 0
    for (lower, upper) in boundaries:
            
        lower = np.array(lower, dtype='uint8')
        upper = np.array(upper, dtype='uint8')

        mask = cv.inRange(hsv, lower, upper)
        mask = cv.dilate(mask, (20,20))
        # cv.imshow("mask", mask)

        out = cv.bitwise_and(img, img, mask=mask)
        cv.imshow("processed", out)
        
        temp = img.copy()
        contours, hier = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv.contourArea(contour)
            if 500 < area: #6200 
                x, y, w, h = cv.boundingRect(contour)
                temp = cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)        
                cv.putText(temp, colours[col_count], (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2) 

                face[(x, y)] = colours[col_count]
                face_wh[(x, y)] = (w, h)

        col_count += 1
        cv.imshow("cube after", temp)
        cv.waitKey(0)

    cv.destroyWindow("cube after")

    # for key in face: 
    #     print(key, face[key])

    # print("----------")

    # for key in face_wh:
    #     print(key, face_wh[key])

    print("----------")

    print(face)
    print(face_wh)
    print(find_squares(face, face_wh))

if __name__ == "__main__":
    # cube_whitebg test 
    # boundaries = [([132, 137, 117], [179, 255, 255]), 
    #         ([96, 102, 60], [166, 255, 255]), 
    #         ([56, 195, 0], [88, 255, 255]), 
    #         ([25, 96, 179], [160, 211, 226]), 
    #         ([0, 160, 178], [17, 255, 255]), 
    #         ([45, 0, 137], [135, 128, 251])]
    
    # img_name = "test_images\cube_whitebg.jpg"
    # calibrate(img_name, boundaries)

    # test images stickerless
    # boundaries = [([178, 167, 120], [179, 255, 180]), 
    #             ([99, 134, 132], [154, 254, 184]), 
    #             ([55, 193, 169], [99, 246, 212]), 
    #             ([28, 162, 180], [40, 221, 220]), 
    #             ([13, 217, 204], [23, 236, 246]), 
    #             ([103, 6, 186], [159, 45, 231])] 
    # img_name = "test_images\cube4.jpg"

    #test images stickered
    boundaries = [([175, 193, 0], [179, 255, 255]), 
                ([93, 157, 110], [143, 255, 255]), 
                ([55, 105, 101], [88, 255, 255]), 
                ([24, 200, 179], [35, 255, 255]),
                ([7, 225, 216], [25, 255, 255]), 
                ([90, 8, 180], [131, 255, 255])]
    img_name = "test_images\stickered.jpg"
    calibrate(img_name, boundaries)





