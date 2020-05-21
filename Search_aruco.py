import cv2
from cv2 import aruco

class SearchAruco:
    def __init__(self, size, first_id, second_id):
        self.aruco_dict = aruco.Dictionary_get(size)
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
        return self.corners

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