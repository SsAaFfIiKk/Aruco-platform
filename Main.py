import cv2
import h5py
from undistort import undistort
from Search_aruco import SearchAruco
from Message_sender import SendMessage

cap = cv2.VideoCapture(0)

# with h5py.File("Camera-corector/parametrs_for_undistort", "r") as f:
#     mtx = f["mtx"][()]
#     dist = f["dist"][()]
#     rvecs = f["rvecs"][()]
#     tvecs = f["tvecs"][()]

detect = SearchAruco(5, 6)
sender = SendMessage()
first_msg = sender.crate_msg("signal", 1)
second_msg = sender.crate_msg("signal", 0)

while True:
    _, frame = cap.read()

    # undistorted = undistort(frame, mtx, dist)

    gray = detect.img_to_gray(frame)
    detect.detect_marker(gray)
    detection_1 = detect.check_first_id()
    detection_2 = detect.check_second_id()
    # detect.info()
    sender.send_first_msg(detection_1, first_msg)
    sender.send_second_msgs(detection_2, second_msg)
    frame_markers = detect.draw_markers(frame)

    cv2.imshow("frame", frame_markers)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
