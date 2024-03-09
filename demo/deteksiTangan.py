from cvzone.HandTrackingModule import HandDetector
import cv2

# Initialize the webcam to capture video
cap = cv2.VideoCapture(0)

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    success, img = cap.read()

    # Find hands in the current frame
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Check if any hands are detected
    if hands:
        for hand in hands:
            # Information for each hand detected
            lmList = hand["lmList"]  # List of 21 landmarks for the hand
            bbox = hand["bbox"]  # Bounding box around the hand (x,y,w,h coordinates)
            center = hand['center']  # Center coordinates of the hand
            handType = hand["type"]  # Type of the hand ("Left" or "Right")

            # Convert handType to "kanan" or "kiri"
            if handType == "Left":
                handType = "Kiri"
            elif handType == "Right":
                handType = "Kanan"

            # Count the number of fingers up for the hand
            fingers = detector.fingersUp(hand)

            # Calculate distance between specific landmarks on the hand and draw it on the image
            length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img, color=(255, 0, 255),
                                                      scale=10)

            # Draw handType on the image with background
            cv2.rectangle(img, (bbox[0]-30, bbox[1] - 60), (bbox[0] + 70, bbox[1] -20), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, handType, (bbox[0]-10, bbox[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # If two hands are detected
        if len(hands) == 2:
            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, img = detector.findDistance(hands[0]["lmList"][8][0:2], hands[1]["lmList"][8][0:2], img,
                                                      color=(255, 0, 0), scale=10)

        print(" ")  # New line for better readability of the printed output

    # Display the image in a window
    cv2.imshow("Image", img)

    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)
