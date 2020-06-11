import cv2
import numpy as np
from cv2 import aruco


class SearchAruco:
    def __init__(self, size, left_id, right_id):
        self.left_id = left_id
        self.right_id = right_id
        self.aruco_dict = aruco.Dictionary_get(size)
        self.parameters = aruco.DetectorParameters_create()
        self.corners = []
        self.ids = []
        self.left_angels = []
        self.right_angels = []
        self.rejectedImgPoints = []
        self.left_x = 0
        self.left_y = 0
        self.right_x = 0
        self.right_y = 0
        self.detect_left = False
        self.detect_right = False

    def img_to_gray(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def detect_marker(self, gray):
        self.corners, self.ids, self.rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict,
                                                                             parameters=self.parameters)

    def draw_markers(self, img):
        frame_markers = aruco.drawDetectedMarkers(img, self.corners, self.ids)
        return frame_markers

    def check_left_id(self):
        if np.all(self.ids != None):
            for k in range(0, len(self.ids)):
                if self.ids[k] == self.left_id:
                    self.detect_left = True
        else:
            self.detect_left = False
        return self.detect_left

    def check_right_id(self):
        if np.all(self.ids != None):
            for k in range(0, len(self.ids)):
                if self.ids[k] == self.right_id:
                    self.detect_right = True
        else:
            self.detect_right = False
        return self.detect_right

    def get_coordinats(self):
        if np.all(self.ids != None):
            for i in range(0, len(self.ids)):
                if len(self.ids) == 1 and self.detect_left:
                    self.left_x = self.corners[0][0][0][0]
                    self.left_y = self.corners[0][0][0][1]

                elif len(self.ids) == 1 and self.detect_right:
                    self.right_x = self.corners[0][0][0][0]
                    self.right_y = self.corners[0][0][0][1]

                else:
                    self.left_x = self.corners[0][0][0][0]
                    self.left_y = self.corners[0][0][0][1]
                    self.right_x = self.corners[1][0][1][0]
                    self.right_y = self.corners[1][0][1][1]

    def get_midle(self):
        self.midl_x = (self.right_x + self.left_x) / 2
        self.midl_y = (self.right_y + self.left_x) / 2

        if self.midl_x < 0:
            self.midl_x *= -1

        if self.midl_y < 0:
            self.midl_y *= -1
        return int(self.midl_x), int(self.midl_y)

    def returning(self):
        return int(self.left_x), int(self.left_y), int(self.right_x), int(self.right_y)

    def info(self):
        if np.all(self.ids != None):
            print(int(self.left_x))
            print(int(self.left_y))
            print(int(self.right_x))
            print(int(self.right_y))
            print(int(self.midl_x))
            print(int(self.midl_y))
