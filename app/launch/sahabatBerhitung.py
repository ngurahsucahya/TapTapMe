import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize the webcam to capture video
cap = cv2.VideoCapture(0)

# Set the initial position of the rectangle
rect_position = [200, 200]
rect_size = 100

# Load the image
image = cv2.imread("../../demo/SucahyaNoBG.png")  # Provide the path to your image file

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5)

# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    success, img = cap.read()
    # img = cv2.flip(img, 1)  # Flip the frame horizontally for intuitive movement

    # Create a green background
    green_background = np.zeros_like(img, dtype=np.uint8)
    green_background[:] = (0, 255, 0)  # Set color to green

    # Find hands in the current frame
    hands, img = detector.findHands(img)

    # Check if any hands are detected
    if hands:
        # Get the landmarks of the first detected hand
        hand_landmarks = hands[0]['lmList']

        # Check if there are landmarks detected for the hand
        if hand_landmarks:
            # Get the position of the index finger (landmark at index 8)
            index_finger_x, index_finger_y = hand_landmarks[8][0], hand_landmarks[8][1]

            # Check if index finger is within the boundaries of the image
            if rect_position[0] < index_finger_x < rect_position[0] + rect_size and \
                    rect_position[1] < index_finger_y < rect_position[1] + rect_size:
                # Update the position of the rectangle based on the index finger position
                rect_position[0] = int(index_finger_x - rect_size / 2)
                rect_position[1] = int(index_finger_y - rect_size / 2)

    # Overlay the image onto the green background
    image_resized = cv2.resize(image, (rect_size, rect_size))
    green_background[rect_position[1]:rect_position[1] + rect_size, rect_position[0]:rect_position[0] + rect_size] = image_resized

    # Display the image in a window
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", green_background)

    # Check for the 'q' key to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
