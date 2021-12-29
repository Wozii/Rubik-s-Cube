import requests
import cv2 as cv
import numpy as np
import imutils

from detect import calibrate
from detect import detect_cube_face

url = "http://192.168.0.159:8080/shot.jpg"

boundaries = [([120, 164, 35], [179, 255, 255]), 
            ([102, 202, 0], [172, 255, 255]), 
            ([59, 195, 28], [82, 255, 255]), 
            ([19, 206, 124], [53, 255, 255]), 
            ([4, 197, 150], [24, 253, 255]), 
            ([78, 25, 47], [98, 64, 182])]

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

def get_faces():
    faces = ["Front", "Back", "Right", "Left", "Top", "Bottom"]
    frames = []
    index = 0   

    lower = np.array((0, 0, 0), dtype='uint8')
    upper = np.array((255, 255, 255), dtype='uint8')
    
    # loop for the live feed
    while True:
        frame = get_frame()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        mask = cv.inRange(hsv, lower, upper)
        mask = cv.dilate(mask, (20, 20))
        out = cv.bitwise_and(frame, frame, mask=mask)

        cv.putText(frame, faces[index], (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv.imshow("Mask", out)
        cv.imshow("Live Feed", frame)
        
        # getting all faces, fix this later to be automatic
        key = cv.waitKey(1) & 0xFF
        if key == 27:
            frames.append(frame)
            if index < 5: 
                index += 1
            else: 
                break
        lower, upper = check_keys(key, lower, upper)
    
    return frames
    
    
def check_keys(key, lower, upper):   
    if key == ord('r'):
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
    
    return lower, upper

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

        boundaries = calibrate(frame)
    
    print("---------------------------")
    print("Here are your boundaries:")
    print(boundaries)
    print("---------------------------")

    faces = get_faces()

    colours = []
    for i in range (len(faces)):
        cube_face = faces[i]
        cv.imshow("faces", cube_face)
        colours.append(detect_cube_face(cube_face, boundaries))
        cv.waitKey(0)

    print("---------------------------")
    print("Here are your cube faces:")
    print(boundaries)
    print("---------------------------")

    cv.destroyAllWindows()

