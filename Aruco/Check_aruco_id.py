import cv2
from cv2 import aruco

# size = aruco.DICT_4X4_250
# size = aruco.DICT_5X5_250
size = aruco.DICT_6X6_250


cap = cv2.VideoCapture(0)
aruco_dict = aruco.Dictionary_get(size)
parameters = aruco.DetectorParameters_create()

while True:

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    cv2.imshow("frame", frame_markers)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()