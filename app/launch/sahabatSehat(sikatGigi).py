import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

#buka kamera, biasanya 3 untuk webcam
cap = cv2.VideoCapture(0)

#sikatGigi, sebenenrya bentuknya kotak
rect1_position = [110, 140]
rect_size = [170, 220]

#kuman1
rect2_position = [300, 200]
rect2_size = [60, 80]

#kuman2
rect3_position = [400, 220]
rect3_size = [60, 80]

sikatGigi = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Sikat gigi.png", cv2.IMREAD_UNCHANGED)
kuman1 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
kuman2 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
bg= cv2.imread("../src/images/mainMenu/BG - Main menu.png", cv2.IMREAD_UNCHANGED)

gigi = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Gigi.png",
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
    image_resized1 = cv2.resize(sikatGigi, (rect_size[0], rect_size[1]))
    sikatGigi_alpha = image_resized1[:, :, 3] / 255.0
    sikatGigi_rgb = image_resized1[:, :, :3]
    for c in range(3):
        green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
        rect1_position[0]:rect1_position[0] + rect_size[0], c] = (
                sikatGigi_rgb[:, :, c] * sikatGigi_alpha +
                green_background[rect1_position[1]:rect1_position[1] + rect_size[1],
                rect1_position[0]:rect1_position[0] + rect_size[0], c] * (1.0 - sikatGigi_alpha))

    # overlay sama bg untuk gambar gigi
    gigi_resized = cv2.resize(gigi, (270, 320))  # Resize gigi fixed size
    rows, cols, channels = gigi_resized.shape

    # set posisi lingkaran
    pos_x = 300
    pos_y = 120  # vertical position

    if channels == 4:
        gigi_rgb = gigi_resized[:, :, :3]  # Extract RGB channels
        gigi_alpha = gigi_resized[:, :, 3]  # Extract alpha channel

        for c in range(3):
            # Check if the pixel is not transparent
            if gigi_alpha.any() != 0:
                green_background[pos_y:pos_y + rows, pos_x:pos_x + cols, c] = gigi_rgb[:, :, c] * (
                        gigi_alpha / 255.0) + \
                                                                              green_background[pos_y:pos_y + rows,
                                                                              pos_x:pos_x + cols, c] * \
                                                                              (1.0 - gigi_alpha / 255.0)
    else:
        green_background[pos_y:pos_y + rows, pos_x:pos_x + cols] = gigi_resized
    # overlay sama bg
    image_resized3 = cv2.resize(kuman2, (rect3_size[0], rect3_size[1]))  # Resize kuman2 rect3_size
    kuman2_alpha = image_resized3[:, :, 3] / 255.0
    kuman2_rgb = image_resized3[:, :, :3]
    for c in range(3):
        green_background[rect3_position[1]:rect3_position[1] + rect3_size[1],
        rect3_position[0]:rect3_position[0] + rect3_size[0], c] = (
                kuman2_rgb[:, :, c] * kuman2_alpha +
                green_background[rect3_position[1]:rect3_position[1] + rect3_size[1],
                rect3_position[0]:rect3_position[0] + rect3_size[0], c] * (1.0 - kuman2_alpha))

    # overlay sama bg untuk gambar kuman1
    image_resized2 = cv2.resize(kuman1, (rect2_size[0], rect2_size[1]))  # Resize kuman1 rect2_size
    kuman1_alpha = image_resized2[:, :, 3] / 255.0
    kuman1_rgb = image_resized2[:, :, :3]
    for c in range(3):
        green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
        rect2_position[0]:rect2_position[0] + rect2_size[0], c] = (
                kuman1_rgb[:, :, c] * kuman1_alpha +
                green_background[rect2_position[1]:rect2_position[1] + rect2_size[1],
                rect2_position[0]:rect2_position[0] + rect2_size[0], c] * (1.0 - kuman1_alpha))

    # overlay sama bg untuk gambar kuman2
    image_resized3 = cv2.resize(kuman2, (rect3_size[0], rect3_size[1]))  # Resize kuman2 rect3_size
    kuman2_alpha = image_resized3[:, :, 3] / 255.0
    kuman2_rgb = image_resized3[:, :, :3]
    for c in range(3):
        green_background[rect3_position[1]:rect3_position[1] + rect3_size[1],
        rect3_position[0]:rect3_position[0] + rect3_size[0], c] = (
                kuman2_rgb[:, :, c] * kuman2_alpha +
                green_background[rect3_position[1]:rect3_position[1] + rect3_size[1],
                rect3_position[0]:rect3_position[0] + rect3_size[0], c] * (1.0 - kuman2_alpha))

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
