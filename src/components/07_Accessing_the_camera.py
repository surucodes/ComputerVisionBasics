import cv2
import sys

s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)
# some ways to use this function:
# cap = cv2.VideoCapture("video.avi") # video.avi is present at the same location
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("images/img_%02d.jpg") #where images folder contains sequences of images
win_name = 'Camera Preview'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

while cv2.waitKey(1) != 27: # Escape
    has_frame, frame = source.read()
    if not has_frame:
        break
    cv2.imshow(win_name, frame)

source.release()
cv2.destroyWindow(win_name)