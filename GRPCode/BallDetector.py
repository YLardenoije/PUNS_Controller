import cv2
import numpy as np

ballMissingFrameThreshold = 50

class BallDetector:
    def __init__(self, video_source=1):
        self.running = True
        self.ballMissFrame = 0
        self.ballMissing = False
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video source {video_source}")
        for i in range(30):
            _, frame = self.cap.read()
        self.maskImageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.maskSat = cv2.split(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))[1]
        self.maskImageGray = cv2.GaussianBlur(self.maskImageGray, (5, 5), 1.4)

    def DetectCircle(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (5, 5), 1.4)
        #Get only saturation channel
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        _, Sat, value = cv2.split(hsv)
        rows = Sat.shape[0]
        subtractedImage = cv2.subtract(Sat, self.maskImageGray)
        subtractedImageInverted = cv2.bitwise_not(subtractedImage)
        subtractedImage = cv2.GaussianBlur(subtractedImage, (5, 5), 1.4)
        subtractedImage= cv2.multiply(subtractedImage,1.1)
        gray = cv2.add(gray, subtractedImage)
        gray = cv2.GaussianBlur(gray, (5, 5), 1.4)
        cv2.imshow('gray', Sat)
        cv2.imshow('subtractedINV', subtractedImageInverted)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT_ALT, 1.4, rows / 8, param1=300, param2=0.9, minRadius=20, maxRadius=400)
        imageCopy = image.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                cv2.circle(imageCopy, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv2.circle(imageCopy, center, radius, (255, 0, 255), 3)

        if (circles is not None):
            return imageCopy, len(circles)
        else:
            return imageCopy, 0
    
    def DetectBlobs(self, image):
        subtractedImage = cv2.subtract(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.maskImageGray)
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 100
        params.filterByCircularity = True
        params.minCircularity = 0.1
        params.filterByConvexity = True
        params.minConvexity = 0.9
        params.filterByInertia = True
        params.minInertiaRatio = 0.01
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(image)
        print(len(keypoints))
        imageCopy = cv2.drawKeypoints(subtractedImage, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return imageCopy
    def detect_ball(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            newFrame, circlecount = self.DetectCircle(frame)

            if newFrame is not None:
                cv2.imshow('GoodFrame', newFrame)
            else:
                cv2.imshow('Frame', frame)

            if circlecount > 0:
                self.ballMissFrame = 0
            else:
                self.ballMissFrame += 1

            if self.ballMissFrame >= ballMissingFrameThreshold:
                self.ballMissing = True
            else:
                self.ballMissing = False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = BallDetector()
    detector.detect_ball()