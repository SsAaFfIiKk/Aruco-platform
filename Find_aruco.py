import cv2
import h5py
from cv2 import aruco


with h5py.File("parametrs_for_undistort", "r") as f:
    mtx = f["mtx"][()]
    dist = f["dist"][()]
    rvecs = f["rvecs"][()]
    tvecs = f["tvecs"][()]

def undistort(img, mtx, dist):
    undistorted = cv2.undistort(img, mtx, dist)
    return undistorted


class ArucoDetect:
    def __init__(self):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()
        self.corners = None
        self.ids = None
        self.rejectedImgPoints = None

    def img_to_gray(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def detect_marker(self, gray):
        self.corners, self.ids, self.rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict,
                                                                             parameters=self.parameters)

    def draw_markers(self, img):
        frame_markers = aruco.drawDetectedMarkers(img, self.corners, self.ids)
        return frame_markers


detect = ArucoDetect()

cap = cv2.VideoCapture(2)

while True:
    _, frame = cap.read()

    undistorted = undistort(frame, mtx, dist)

    gray = detect.img_to_gray(undistorted)
    detect.detect_marker(gray)
    frame_markers = detect.draw_markers(undistorted)

    cv2.imshow("frame", frame_markers)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
