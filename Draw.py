import cv2


class Draw:
    def __init__(self):
        self.x = None
        self.y = None
        self.solor = (255, 0, 0)

    def draw_borders(self, img):
        cv2.line(img, (310, 230), (310, 250), self.solor, 3)
        cv2.line(img, (330, 230), (330, 250), self.solor, 3)


