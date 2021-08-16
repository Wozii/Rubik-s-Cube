import requests
import cv2 as cv
import numpy as np
import imutils
  
url = "http://192.168.0.159:8080/shot.jpg"

# while True:
img_resp = requests.get(url)
img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
img = cv.imdecode(img_arr, -1)
img = imutils.resize(img, width=1000, height=1800)
cv.imshow("Android_cam", img)


cv.waitKey(0)
    # # Press Esc key to exit
    # if cv.waitKey(1) == 27:
    #     break
  
cv.destroyAllWindows()