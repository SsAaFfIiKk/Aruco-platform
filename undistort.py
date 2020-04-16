def undistort(img, mtx, dist):
    undistorted = cv2.undistort(img, mtx, dist)
    return undistorted