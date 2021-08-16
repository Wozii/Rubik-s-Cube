import cv2 as cv
import numpy as np

xy_points = []
confirm = False

def outline_colour(event, x, y, flags, param):
    global xy_points, confirm

    if event == cv.EVENT_LBUTTONDOWN:
        xy_points = [(x, y)]
    
    elif event == cv.EVENT_LBUTTONUP:
        xy_points.append((x, y))
        cv.rectangle(img, xy_points[0], xy_points[1], (0, 255, 0), 2)
        cv.imshow("image", img)
    

def get_boundaries(img, x1, y1, x2, y2):
    print(x1, y1)
    print(x2, y2)
    lower = np.array(img[x1, y1])
    upper = np.array(img[x1, y1])    

    print('comparing')

    for i in range(x1, x2):
        for j in range(y1, y2):
            check = np.array(img[i, j])

            for k in range(0, 3):
                if check[k] < lower[k]:
                    print(k, check[k], lower[k])
                    lower[k] = check[k]
                elif check[k] > upper[k]:
                    upper[k] = check[k]


            # if np.less(check, lower).all():
            #     print("lower", lower, check)
            #     lower = check
            # elif np.greater(check, upper).all():
            #     print("upper", upper, check)
            #     upper = check

    return lower, upper

boundaries = []
cube1 = cv.imread('cube_whitebg.jpg')
img = cv.resize(cube1, (300, 400), interpolation=cv.INTER_AREA)
clone = img.copy()

cv.namedWindow("image")
cv.setMouseCallback("image", outline_colour)

while len(boundaries) != 6: 
    while True: 
        cv.imshow("image", img)
        key = cv.waitKey(1) & 0xFF

        if key == ord("x"):
            img = clone.copy()
        elif key == ord("c"):
            break

    if len(xy_points) == 2:
        crop = clone[xy_points[0][1]:xy_points[1][1], xy_points[0][0]:xy_points[1][0]]
        cv.imshow("crop", crop)

        # print(xy_points[0], xy_points[1])
        # print(clone[xy_points[0]], clone[xy_points[1]])
        cv.waitKey(0)

        lower, upper = get_boundaries(clone, xy_points[0][0], xy_points[0][1], xy_points[1][0], xy_points[1][1])
        print("new colour:")
        print(lower, upper)
        boundaries.append((lower.tolist(), upper.tolist()))

print(boundaries)

cv.destroyAllWindows()


img = clone.copy()
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

count = 1
for (lower, upper) in boundaries:
    # (lower, upper) = boundaries[4]
        
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    mask = cv.inRange(img, lower, upper)
    mask = cv.dilate(mask, (5,5))
    # cv.imshow("mask", mask)

    out = cv.bitwise_and(img, img, mask=mask)
    cv.imshow("processed" + str(count), out)
    
    temp = img.copy()
    contours, hier = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if 500 < area < 6200: 
            x, y, w, h = cv.boundingRect(contour)
            temp = cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
            cv.putText(temp, "a", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255)) 

    cv.imshow("cube after" + str(count), temp)
    count+= 1



cv.waitKey(0)
