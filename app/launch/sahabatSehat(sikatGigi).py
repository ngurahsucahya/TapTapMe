import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

#buka kamera, biasanya 3 untuk webcam
cap = cv2.VideoCapture(0)

#bola1, sebenenrya bentuknya kotak
rect1_position = [110, 140]
rect_size = [170, 220]

#bola2
rect2_position = [80, 170]
rect2_size = [170, 220]

#bola3
rect3_position = [130, 200]
rect3_size = [170, 220]

bola1 = cv2.imread("../src/images/Bola.png", cv2.IMREAD_UNCHANGED)
bola2 = cv2.imread("../src/images/Bola.png", cv2.IMREAD_UNCHANGED)
bola3 = cv2.imread("../src/images/Bola.png", cv2.IMREAD_UNCHANGED)
bg= cv2.imread("../src/images/mainMenu/BG - Main menu.png", cv2.IMREAD_UNCHANGED)

lingkaranBenar = cv2.imread("../src/images/circle.png",
                          cv2.IMREAD_UNCHANGED)

pertanyaan = cv2.imread("../src/images/Ambil 1 bola.png",
                          cv2.IMREAD_UNCHANGED)

#deteksi tangan
detector = HandDetector(staticMode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5)

#pokoknya ngambil framenya disini
while True:
    success, img = cap.read()

    green_background = np.zeros_like(img, dtype=np.uint8)
    green_background[:] = (255, 255, 255)

    image_resized3 = cv2.resize(bg, (img.shape[1], img.shape[0]))  # Resize bg full screen
    bg_alpha = image_resized3[:, :, 3] / 255.0
    bg_rgb = image_resized3[:, :, :3]
    for c in range(3):
        green_background[:, :, c] = (
                bg_rgb[:, :, c] * bg_alpha +
                green_background[:, :, c] * (1.0 - bg_alpha))

    # baca tangan lagi fimana
    hands, img = detector.findHands(img)
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
    image_resized3 = cv2.resize(bola3, (rect3_size[0], rect3_size[1]))  # Resize bola3 rect3_size
    bola3_alpha = image_resized3[:, :, 3] / 255.0
    bola3_rgb = image_resized3[:, :, :3]
    for c in range(3):
        green_background[rect3_position[1]:rect3_position[1] + rect3_size[1],
        rect3_position[0]:rect3_position[0] + rect3_size[0], c] = (
                bola3_rgb[:, :, c] * bola3_alpha +
                green_background[rect3_position[1]:rect3_position[1] + rect3_size[1],
                rect3_position[0]:rect3_position[0] + rect3_size[0], c] * (1.0 - bola3_alpha))

    # overlay sama bg
    image_resized2 = cv2.resize(bola2, (rect2_size[0], rect2_size[1]))  # Resize bola2 rect2_size
    bola2_alpha = image_resized2[:, :, 3] / 255.0
    bola2_rgb = image_resized2[:, :, :3]
    for c in range(3):
        green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
        rect2_position[0]:rect2_position[0] + rect2_size[0], c] = (
                bola2_rgb[:, :, c] * bola2_alpha +
                green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
                rect2_position[0]:rect2_position[0] + rect2_size[0], c] * (1.0 - bola2_alpha))

    # overlay sama bg
    image_resized1 = cv2.resize(bola1, (rect_size[0], rect_size[1]))
    bola1_alpha = image_resized1[:, :, 3] / 255.0
    bola1_rgb = image_resized1[:, :, :3]
    for c in range(3):
        green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
        rect1_position[0]:rect1_position[0] + rect_size[0], c] = (
                bola1_rgb[:, :, c] * bola1_alpha +
                green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
                rect1_position[0]:rect1_position[0] + rect_size[0], c] * (1.0 - bola1_alpha))

    # overlay sama bg
    lingkaranBenar_resized = cv2.resize(lingkaranBenar, (270, 320))  # Resize lingkaranBenar fixed size
    rows, cols, channels = lingkaranBenar_resized.shape

    # set posisi lingkaran
    pos_x = 300
    pos_y = 120  #vertical position

    if channels == 4:
        lingkaranBenar_rgb = lingkaranBenar_resized[:, :, :3]  # Extract RGB channels
        lingkaranBenar_alpha = lingkaranBenar_resized[:, :, 3]  # Extract alpha channel

        for c in range(3):
            green_background[pos_y:pos_y + rows, pos_x:pos_x + cols, c] = lingkaranBenar_rgb[:, :, c] * (
                    lingkaranBenar_alpha / 255.0) + \
                                                                          green_background[pos_y:pos_y + rows,
                                                                          pos_x:pos_x + cols, c] * \
                                                                          (1.0 - lingkaranBenar_alpha / 255.0)
    else:
        green_background[pos_y:pos_y + rows, pos_x:pos_x + cols] = lingkaranBenar_resized

    pertanyaan_resized = cv2.resize(pertanyaan, (380, 140))
    rows, cols, channels = pertanyaan_resized.shape

    #posisi pertanyaan
    pos_x = 135
    pos_y = 5

    if channels == 4:
        pertanyaan_rgb = pertanyaan_resized[:, :, :3]  # Extract RGB channels
        pertanyaan_alpha = pertanyaan_resized[:, :, 3]  # Extract alpha channel

        for c in range(3):
            green_background[pos_y:pos_y + rows, pos_x:pos_x + cols, c] = pertanyaan_rgb[:, :, c] * (
                    pertanyaan_alpha / 255.0) + \
                                                                          green_background[pos_y:pos_y + rows,
                                                                          pos_x:pos_x + cols, c] * \
                                                                          (1.0 - pertanyaan_alpha / 255.0)
    else:
        green_background[pos_y:pos_y + rows, pos_x:pos_x + cols] = pertanyaan_resized


    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", green_background)

   #keluar programnya
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#selesai
cap.release()
cv2.destroyAllWindows()
