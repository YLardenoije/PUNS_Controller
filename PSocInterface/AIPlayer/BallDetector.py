import cv2
import numpy as np

class BallDetector:
    def __init__(self, video_source=0):
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

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT_ALT, 1.4, rows / 8, param1=300, param2=0.9, minRadius=1, maxRadius=400)
        imageCopy = image.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                cv2.circle(imageCopy, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv2.circle(imageCopy, center, radius, (255, 0, 255), 3)
        return imageCopy
    
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
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            annotatedFrame = self.DetectCircle(frame)
            #self.maskImageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # lower_bound = np.array([30, 150, 50])
            # upper_bound = np.array([255, 255, 180])
            # mask = cv2.inRange(hsv, lower_bound, upper_bound)
            # res = cv2.bitwise_and(frame, frame, mask=mask)

            # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # for contour in contours:
            #     area = cv2.contourArea(contour)
            #     if area > 500:
            #         x, y, w, h = cv2.boundingRect(contour)
            #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if annotatedFrame is not None:
                cv2.imshow('GoodFrame', annotatedFrame)
            else:
                cv2.imshow('Frame', frame)
            # cv2.imshow('Mask', mask)
            # cv2.imshow('Result', res)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = BallDetector()
    detector.detect_ball()