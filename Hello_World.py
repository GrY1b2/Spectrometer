import cv2

cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

img_counter = 0
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    (h, w, _) = frame.shape
    print(h,w)

    for i in range(h):
        for j in range(w):
            (r, g, b) = frame[i,j]
            if not (r < 50 and g < 50 and b < 50):
                print("Black {}, {}".format(i,j))



    cv2.imshow("test", frame)

    k = cv2.waitKey(0)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()

