import cv2
from cv2 import line

class Draw:
    def __init__(self):
        self.blue = (255, 0, 0)
        self.red = (0, 0, 255)

    def draw_borders(self, img, size, coords):
        pt1 = (coords[0] - size, coords[1])
        pt2 = (coords[0] + size, coords[1])
        pt3 = (coords[0], coords[1] - size)
        pt4 = (coords[0], coords[1] + size)
        line(img, pt1, pt2, (0, 50, 255), 2)
        line(img, pt3, pt4, (0, 50, 255), 2)
        cv2.line(img, (310, 230), (310, 250), self.red, 3)
        cv2.line(img, (330, 230), (330, 250), self.red, 3)

    def draw_points(self, img, l_x, l_y, r_x, r_y):
        cv2.circle(img, (l_x, l_y), 2, self.red, -1)
        cv2.circle(img, (r_x, r_y), 2, self.red, -1)

    def draw_midle(self,img, m_x, m_y):
        cv2.circle(img, (m_x, m_y), 4, self.blue, -1)

    def put(self, img, text, coords, font):
        cv2.putText(img, text, coords, font, 1, (0, 255, 0), 2, cv2.LINE_AA)
