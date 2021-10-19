import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

ret, frame = cam.read()
if not ret:
    print("failed to grab frame")

(h, w, _) = frame.shape
for i in range(h):
    for j in range(w):
        print(frame[i,j])


cv2.imshow("test", frame)

k = cv2.waitKey(0)
if k%256 == 27:
    # ESC pressed
    print("Escape hit, closing...")

cam.release()

cv2.destroyAllWindows()