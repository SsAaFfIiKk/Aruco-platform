import cv2
import h5py
import  math
from cv2 import aruco
from Undistort import undistort
from Search_aruco import SearchAruco
from Message_sender import SendMessage

with h5py.File("Camera-corector/parametrs_for_undistort.h5py", "r") as f:
    mtx = f["mtx"][()]
    dist = f["dist"][()]
    rvecs = f["rvecs"][()]
    tvecs = f["tvecs"][()]


# size = aruco.DICT_4X4_250
# size = aruco.DICT_5X5_250
size = aruco.DICT_6X6_250
detect = SearchAruco(size, 5, 6)

# sender = SendMessage()
# first_msg = sender.crate_msg("signal", 1)
# second_msg = sender.crate_msg("signal", 0)

corners = None

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    undistorted = undistort(frame, mtx, dist)

    gray = detect.img_to_gray(frame)
    corners = detect.detect_marker(gray)
    detection_1 = detect.check_first_id()
    detection_2 = detect.check_second_id()
    # detect.info()
    # sender.send_first_msg(detection_1, first_msg)
    # sender.send_second_msgs(detection_2, second_msg)
    frame_markers = detect.draw_markers(frame)

    cv2.imshow("frame", frame_markers)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
