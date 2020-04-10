import cv2
import h5py
from cv2 import aruco
from paho.mqtt import publish


# with h5py.File("parametrs_for_undistort", "r") as f:
#     mtx = f["mtx"][()]
#     dist = f["dist"][()]
#     rvecs = f["rvecs"][()]
#     tvecs = f["tvecs"][()]


def undistort(img, mtx, dist):
    undistorted = cv2.undistort(img, mtx, dist)
    return undistorted

cap = cv2.VideoCapture(0)



class ArucoDetect:
    def __init__(self, first_id, second_id):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()
        self.corners = None
        self.ids = None
        self.rejectedImgPoints = None
        self.detect_1 = False
        self.detect_2 = False
        self.first_id = first_id
        self.second_id = second_id
        self.send_1 = False
        self.send_2 = False
        self.msgs_1 = [{"topic": "signal", "payload": "first signal"}]
        self.msgs_2 = [{"topic": "signal", "payload": "second signal "}]

    def img_to_gray(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def detect_marker(self, gray):
        self.corners, self.ids, self.rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict,
                                                                             parameters=self.parameters)
    def draw_markers(self, img):
        frame_markers = aruco.drawDetectedMarkers(img, self.corners, self.ids)
        return frame_markers

    def check_first_id(self):
        if self.ids is not None:
            for k in range(0, len(self.ids)):
                if self.ids[k] == self.first_id:
                    self.detect_1 = True
        else:
            self.detect_1 = False

    def check_second_id(self):
        if self.ids is not None:
            for k in range(0, len(self.ids)):
                if self.ids[k] == self.second_id:
                    self.detect_2 = True
        else:
            self.detect_2 = False

    def send_first_msgs(self):
        if self.send_1 == False and self.detect_1 == True:
            publish.multiple(self.msgs_1, hostname="localhost")
            self.send_1 = True

    def send_second_msgs(self):
        if self.send_2 == False and self.detect_2 == True:
            publish.multiple(self.msgs_2, hostname="localhost")
            self.send_2 = True

    def output(self):
        if self.detect_1 and self.detect_2:
            print("See both")

        elif self.detect_1:
            print("See id" + str(self.first_id) + " marker")
            self.send_first_msgs()

        elif self.detect_2:
            print("See id" + str(self.second_id) + " marker")
            self.send_second_msgs()

        # elif self.detect_1 == False and self.detect_2 == False:
        #     print("Don't see markers")


detect = ArucoDetect(5, 6)

while True:
    _, frame = cap.read()

    # undistorted = undistort(frame, mtx, dist)

    gray = detect.img_to_gray(frame)
    detect.detect_marker(gray)
    detect.check_first_id()
    detect.check_second_id()
    detect.output()
    frame_markers = detect.draw_markers(frame)

    cv2.imshow("frame", frame_markers)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
