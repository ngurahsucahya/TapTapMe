import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize the webcam to capture video
cap = cv2.VideoCapture(0)

# Set the initial position and size of the first rectangle
rect1_position = [80, 200]
rect_size = [60,90]

# Set the initial position and size of the second rectangle
rect2_position = [480, 200]
rect2_size = [90,50]  # Change rect2_size to a list containing width and height

# Load the bagianTubuh
bagianTubuh1 = cv2.imread("../src/images/Telinga.png", cv2.IMREAD_UNCHANGED)  # Provide the path to your first bagianTubuh file
bagianTubuh2 = cv2.imread("../src/images/Mata.png", cv2.IMREAD_UNCHANGED)  # Provide the path to your second bagianTubuh file

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5)

# Continuously get frames from the webcam
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

            # Check if index finger is within the boundaries of the first bagianTubuh
            if rect1_position[0] < index_finger_x < rect1_position[0] + rect_size[0] and \
                    rect1_position[1] < index_finger_y < rect1_position[1] + rect_size[1]:
                # Update the position of the first rectangle based on the index finger position
                rect1_position[0] = int(index_finger_x - rect_size[0] / 2)
                rect1_position[1] = int(index_finger_y - rect_size[1] / 2)

            # Check if index finger is within the boundaries of the second bagianTubuh
            elif rect2_position[0] < index_finger_x < rect2_position[0] + rect2_size[0] and \
                    rect2_position[1] < index_finger_y < rect2_position[1] + rect2_size[1]:
                # Update the position of the second rectangle based on the index finger position
                rect2_position[0] = int(index_finger_x - rect2_size[0] / 2)
                rect2_position[1] = int(index_finger_y - rect2_size[1] / 2)

    # Boundary check for the first rectangle
    rect1_position[0] = max(0, min(rect1_position[0], img.shape[1] - rect_size[0]))
    rect1_position[1] = max(0, min(rect1_position[1], img.shape[0] - rect_size[1]))

    # Boundary check for the second rectangle
    rect2_position[0] = max(0, min(rect2_position[0], img.shape[1] - rect2_size[0]))
    rect2_position[1] = max(0, min(rect2_position[1], img.shape[0] - rect2_size[1]))

    # Overlay the first bagianTubuh onto the green background
    image_resized1 = cv2.resize(bagianTubuh1, (rect_size[0], rect_size[1]))
    bagianTubuh1_alpha = image_resized1[:, :, 3] / 255.0
    bagianTubuh1_rgb = image_resized1[:, :, :3]
    for c in range(3):
        green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
                         rect1_position[0]:rect1_position[0] + rect_size[0], c] = (
                    bagianTubuh1_rgb[:, :, c] * bagianTubuh1_alpha +
                    green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
                                     rect1_position[0]:rect1_position[0] + rect_size[0], c] * (1.0 - bagianTubuh1_alpha))

    # Overlay the second bagianTubuh onto the green background
    image_resized2 = cv2.resize(bagianTubuh2, (rect2_size[0], rect2_size[1]))  # Resize bagianTubuh2 to match rect2_size
    bagianTubuh2_alpha = image_resized2[:, :, 3] / 255.0
    bagianTubuh2_rgb = image_resized2[:, :, :3]
    for c in range(3):
        # Check if the region of overlay exceeds the bounds of the background
        if (rect2_position[1] + rect2_size[1]) <= green_background.shape[0] and (rect2_position[0] + rect2_size[0]) <= \
                green_background.shape[1]:
            green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
            rect2_position[0]:rect2_position[0] + rect2_size[0], c] = (
                    bagianTubuh2_rgb[:, :, c] * bagianTubuh2_alpha +
                    green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
                                    rect2_position[0]:rect2_position[0] + rect2_size[0], c] * (1.0 - bagianTubuh2_alpha))
    # Display the combined bagianTubuh in a window
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", green_background)

    # Check for the 'q' key to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
