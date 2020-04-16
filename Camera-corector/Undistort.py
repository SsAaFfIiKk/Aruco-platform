import os
import cv2
import h5py
import numpy as np

objpoints = []
imgpoints = []
imgs = []

imgs_folder = "set_0"
img_num = 0
img_size = None
photos_lst = os.listdir(imgs_folder)

rows = 6
cols = 9

objp = np.zeros((rows * cols, 3), np.float32)
objp[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cam = cv2.VideoCapture(2)

while len(imgs) < len(photos_lst):
    img_name = str(img_num) + "_veb.png"

    img = cv2.imread(os.path.join(imgs_folder, img_name))
    imgs.append(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (rows, cols))

    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, (rows, cols), corners, ret)
        objpoints.append(objp)


# показывает нахождение доски
    cv2.imshow(str(img_num), img)
    cv2.waitKey(420)
    cv2.destroyAllWindows()

    img_num += 1
    img_size = gray.shape[::-1]


# калибровка камеры
_, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

# применеие новых параметров чтобы исправить изображения
while True:
    _, frame = cam.read()

    undistorted = cv2.undistort(frame, mtx, dist)

    cv2.imshow("Orig", frame)
    cv2.imshow("Undistorted", undistorted)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    elif cv2.waitKey(1) & 0xFf == ord("s"):
        with h5py.File("parametrs_for_undistort", "w") as f:
            f.create_dataset("mtx", data=mtx)
            f.create_dataset("dist", data=dist)
            f.create_dataset("rvecs", data=rvecs)
            f.create_dataset("tvecs", data=tvecs)
        break

cam.release()
cv2.destroyAllWindows()
