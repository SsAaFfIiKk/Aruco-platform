import cv2
import h5py
from cv2 import aruco
from paho.mqtt import publish

cap = cv2.VideoCapture(0)

# with h5py.File("parametrs_for_undistort", "r") as f:
#     mtx = f["mtx"][()]
#     dist = f["dist"][()]
#     rvecs = f["rvecs"][()]
#     tvecs = f["tvecs"][()]


def undistort(img, mtx, dist):
    undistorted = cv2.undistort(img, mtx, dist)
    return undistorted


class SearchAruco:
    def __init__(self, first_id, second_id):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()
        self.corners = None
        self.ids = None
        self.rejectedImgPoints = None
        self.detect_first = False
        self.detect_second = False
        self.first_id = first_id
        self.second_id = second_id

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
                    self.detect_first = True
        else:
            self.detect_first = False
        return self.detect_first

    def check_second_id(self):
        if self.ids is not None:
            for k in range(0, len(self.ids)):
                if self.ids[k] == self.second_id:
                    self.detect_second = True
        else:
            self.detect_second = False
        return self.detect_second

    def info(self):
        if self.detect_first and self.detect_second:
            print("See both")

        elif self.detect_first:
            print("See id" + str(self.first_id) + " marker")

        elif self.detect_second:
            print("See id" + str(self.second_id) + " marker")

        elif self.detect_first and self.detect_second == False:
            print("Don't see markers")


class SendMessage():
    def __init__(self):
        self.send_first = False
        self.send_second = False

    def crate_msg(self, topic, msg):
        message = [{"topic": topic, "payload": msg}]
        return message

    def send_first_msg(self, detect_first, message):
        if self.send_first == False and detect_first == True:
            publish.multiple(message, hostname="localhost")
            self.send_first = True

    def send_second_msgs(self, detect_second, message):
        if self.send_second == False and detect_second == True:
            publish.multiple(message, hostname="localhost")
            self.send_second = True


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
    detect.info()
    sender.send_first_msg(detection_1, first_msg)
    sender.send_second_msgs(detection_2,second_msg)
    frame_markers = detect.draw_markers(frame)

    cv2.imshow("frame", frame_markers)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
