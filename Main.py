import cv2
import h5py
import math
import numpy as np
from cv2 import aruco
from Draw import Draw
from Undistort import undistort
from Search_aruco import SearchAruco
from Message_sender import SendMessage

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
mqtt = SendMessage("localhost")
turn_left = mqtt.crate_msg("signal", "L")
turn_right = mqtt.crate_msg("signal", "R")
forward = mqtt.crate_msg("signal", "F")
stop = mqtt.crate_msg("signal", "S")


ang = 0
top_point = (320, 140)
bot_point = (320, 460)
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)


def get_angel(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return round(ang)

def decison(ang, l_id, r_id):
    status = "not ready to docking"
    mqtt.send_msg(stop)
    if l_id and r_id and -2 < ang < 2:
        status = "ready to docking"
        mqtt.send_msg(forward)
    elif l_id and r_id and ang <= -3:
        status = "need to turn right"
        mqtt.send_msg(turn_right)
    elif l_id and r_id and ang >= 3:
        status = "need to turn left"
        mqtt.send_msg(turn_left)
    return status

while True:
    _, frame = cap.read()

    undistorted = undistort(frame, mtx, dist)
    gray = detect.img_to_gray(undistorted)
    detect.detect_marker(gray)
    copy = np.copy(undistorted)
    l_id = detect.check_left_id()
    r_id = detect.check_right_id()
    detect.get_coordinats()
    frame_markers = detect.draw_markers(undistorted)

    m_x, m_y = detect.get_midle()
    l_x, l_y, r_x, r_y = detect.returning()
    if m_x and m_y != 0:
        ang = get_angel(top_point, bot_point, (m_x, m_y))

    status = decison(ang,l_id, r_id)

    draw.draw_borders(copy, 5, bot_point)
    draw.draw_points(copy, l_x, l_y, r_x, r_y)
    draw.draw_midle(copy, m_x, m_y)
    draw.put(copy, "Angle: " + str(ang), (0, 34), font)
    draw.put(copy, status, (230, 34), font)

    cv2.imshow("markers", frame_markers)
    cv2.imshow("undistort", copy)
    # detect.info()

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
