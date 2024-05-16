import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

#bagianTubuh1
rect1_position = [80, 200]
rect_size = [60, 90]

#bagianTubuh2
rect2_position = [480, 200]
rect2_size = [90, 50]

bagianTubuh1 = cv2.imread("../src/images/Telinga.png",
                          cv2.IMREAD_UNCHANGED)
bagianTubuh2 = cv2.imread("../src/images/Mata.png",
                          cv2.IMREAD_UNCHANGED)
bagianTubuh3 = cv2.imread("../src/images/Fullbody.png",
                          cv2.IMREAD_UNCHANGED)


#deteksi tangan
detector = HandDetector(staticMode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5)

#pokoknya ngambil framenya disini
while True:
    success, img = cap.read()

    green_background = np.zeros_like(img, dtype=np.uint8)
    green_background[:] = (255, 255, 255)

    hands, img = detector.findHands(img)

    # baca tangan lagi fimana
    if hands:
        hand_landmarks = hands[0]['lmList']

        if hand_landmarks:

            index_finger_x, index_finger_y = hand_landmarks[8][0], hand_landmarks[8][1]

            if rect1_position[0] < index_finger_x < rect1_position[0] + rect_size[0] and \
                    rect1_position[1] < index_finger_y < rect1_position[1] + rect_size[1]:
                rect1_position[0] = int(index_finger_x - rect_size[0] / 2)
                rect1_position[1] = int(index_finger_y - rect_size[1] / 2)

            elif rect2_position[0] < index_finger_x < rect2_position[0] + rect2_size[0] and \
                    rect2_position[1] < index_finger_y < rect2_position[1] + rect2_size[1]:
                rect2_position[0] = int(index_finger_x - rect2_size[0] / 2)
                rect2_position[1] = int(index_finger_y - rect2_size[1] / 2)

    # overlay sama bg
    image_resized1 = cv2.resize(bagianTubuh1, (rect_size[0], rect_size[1]))
    bagianTubuh1_alpha = image_resized1[:, :, 3] / 255.0
    bagianTubuh1_rgb = image_resized1[:, :, :3]
    for c in range(3):
        green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
        rect1_position[0]:rect1_position[0] + rect_size[0], c] = (
                bagianTubuh1_rgb[:, :, c] * bagianTubuh1_alpha +
                green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
                rect1_position[0]:rect1_position[0] + rect_size[0], c] * (1.0 - bagianTubuh1_alpha))

    # overlay sama bg
    image_resized2 = cv2.resize(bagianTubuh2, (rect2_size[0], rect2_size[1]))
    bagianTubuh2_alpha = image_resized2[:, :, 3] / 255.0
    bagianTubuh2_rgb = image_resized2[:, :, :3]
    for c in range(3):
        green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
        rect2_position[0]:rect2_position[0] + rect2_size[0], c] = (
                bagianTubuh2_rgb[:, :, c] * bagianTubuh2_alpha +
                green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
                rect2_position[0]:rect2_position[0] + rect2_size[0], c] * (1.0 - bagianTubuh2_alpha))

    bagianTubuh3_resized = cv2.resize(bagianTubuh3, (270, 430))  # Resize bagianTubuh3 to a fixed size
    rows, cols, channels = bagianTubuh3_resized.shape

    # posisi pertanyaan bagianTubuh3
    pos_x = 180
    pos_y = 30

    if channels == 4:
        bagianTubuh3_rgb = bagianTubuh3_resized[:, :, :3]  # Extract RGB channels
        bagianTubuh3_alpha = bagianTubuh3_resized[:, :, 3]  # Extract alpha channel

        for c in range(3):
            green_background[pos_y:pos_y + rows, pos_x:pos_x + cols, c] = bagianTubuh3_rgb[:, :, c] * (
                        bagianTubuh3_alpha / 255.0) + \
                        green_background[pos_y:pos_y + rows,
                        pos_x:pos_x + cols, c] * \
                        (1.0 - bagianTubuh3_alpha / 255.0)
    else:
        green_background[pos_y:pos_y + rows, pos_x:pos_x + cols] = bagianTubuh3_resized

    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", green_background)

    #keluar programnya
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#selesai
cap.release()
cv2.destroyAllWindows()
