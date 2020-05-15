# ref: https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv
import sys
import cv2
def capture_camera(num=0):
    """Capture video from camera"""
    # カメラをキャプチャする
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("opencv frame {}".format(num))

    ret, frame = cam.read()
    if not ret:
        print('not found camera')
        return
    k = cv2.waitKey(1)

    img_name = "opencv_frame_{}.png".format(num)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))

    cam.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    num = sys.argv[1] if len(sys.argv) >= 2 else 0
    capture_camera(num)