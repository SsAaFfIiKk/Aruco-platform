import cv2
import h5py
import numpy as np
from cv2 import aruco
from Undistort import undistort
from Search_aruco import SearchAruco
from Draw import Draw
# from Message_sender import SendMessage

with h5py.File("Camera-corector/parametrs_for_undistort.h5py", "r") as f:
    mtx = f["mtx"][()]
    dist = f["dist"][()]
    rvecs = f["rvecs"][()]
    tvecs = f["tvecs"][()]


# size = aruco.DICT_4X4_250
size = aruco.DICT_5X5_250
# size = aruco.DICT_6X6_250

detect = SearchAruco(size, 11, 12)
draw = Draw()

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    undistorted = undistort(frame, mtx, dist)
    gray = detect.img_to_gray(undistorted)
    copy = np.copy(undistorted)
    detect.detect_marker(gray)
    detect.check_left_id()
    detect.check_right_id()
    detect.get_coordinats()
    frame_markers = detect.draw_markers(undistorted)
    m_x , m_y =detect.calculate()
    l_x, l_y, r_x, r_y = detect.returning()

    draw.draw_borders(copy)
    draw.draw_points(copy, l_x, l_y, r_x, r_y)
    draw.draw_midle(copy, m_x, m_y)

    cv2.imshow("markers", frame_markers)
    cv2.imshow("undistort", copy)
    # detect.info()

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
