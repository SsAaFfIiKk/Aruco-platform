import os
import cv2
import numpy as np
from time import time


def save_images(frame, f_number):
    str_f_number = str(f_number)
    path_to_save = os.path.join(folder_sav, str_f_number)
    cv2.imwrite(path_to_save + "_veb.png", frame)
    print(str_f_number + " is save")
    if str_f_number == str(29):
        print("save complete")


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

frame_number = 0
save = False
folder_sav = ""
direct = os.listdir()

if "set_0" not in direct:
    os.mkdir("set_0")
    folder_sav = "set_0"
else:
    for i in direct:
        if len(i) >= 5:
            if i[:4] == "set_":
                x = i[4:]
                y = int(x) + 1
                folder_sav = i[:4] + str(y)
            if folder_sav in direct:
                x = folder_sav[4:]
                y = int(x) + 1
                folder_sav = folder_sav[:4] + str(y)
    os.mkdir(folder_sav)

cam = cv2.VideoCapture(0)

st_time = time()
while True:
    _, frame = cam.read()

    F = np.copy(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)

    if ret:

        cor = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        chest_r = cv2.drawChessboardCorners(F, (6, 9), cor, ret)

    cv2.imshow("Frame", F)
    end_time = time()

    if frame_number < 30 and ret:
        save = True
    elif frame_number > 29:
        save = False
    else:
        st_time = time()

    if save:
        if end_time - st_time > 5:
            save_images(frame, frame_number)
            frame_number += 1
            st_time = time()

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
