from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

# size = aruco.DICT_4X4_250
# size = aruco.DICT_5X5_250
size = aruco.DICT_6X6_250

aruco_dict = aruco.Dictionary_get(size)

fig = plt.figure()
nx = 4
ny = 3
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict,i, 700)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")

plt.savefig("markers5x5.png")
plt.show()
