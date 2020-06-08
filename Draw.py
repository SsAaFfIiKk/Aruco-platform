import cv2
from cv2 import line

class Draw:
    def __init__(self):
        self.blue = (255, 0, 0)
        self.red = (0, 0, 255)

    def draw_borders(self, img):
        size = 15
        pt1 = (320 - size, 240)
        pt2 = (320 + size, 240)
        pt3 = (320, 240 - size)
        pt4 = (320, 240 + size)
        line(img, pt1, pt2, (0, 50, 255), 2)
        line(img, pt3, pt4, (0, 50, 255), 2)

    def draw_points(self, img, l_x, l_y, r_x, r_y):
        cv2.circle(img, (l_x, l_y), 2, self.red, -1)
        cv2.circle(img, (r_x, r_y), 2, self.red, -1)

    def draw_midle(self,img, m_x, m_y):
        cv2.circle(img, (m_x, m_y), 4, self.blue, -1)