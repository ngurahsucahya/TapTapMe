import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Buka kamera, biasanya 0 untuk webcam
cap = cv2.VideoCapture(0)

# sikatGigi, sebenarnya bentuknya kotak
rect1_position = [110, 140]
rect_size = [170, 220]

# kuman1
rect2_position = [300, 200]
rect2_size = [60, 80]
kuman1_visible = True  # Visibility flag for kuman1

# kuman2
rect3_position = [400, 220]
rect3_size = [60, 80]
kuman2_visible = True  # Visibility flag for kuman2

sikatGigi = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Sikat gigi.png", cv2.IMREAD_UNCHANGED)
kuman1 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
kuman2 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
bg = cv2.imread("../src/images/mainMenu/BG - Main menu.png", cv2.IMREAD_UNCHANGED)

gigi = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Gigi.png", cv2.IMREAD_UNCHANGED)

pertanyaan = cv2.imread("../src/images/Ambil 1 bola.png", cv2.IMREAD_UNCHANGED)

# deteksi tangan
detector = HandDetector(staticMode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5)

def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay img_overlay on top of img at (x, y) and blend using alpha_mask."""
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]

    img[y1:y2, x1:x2] = alpha * img_overlay_crop + (1 - alpha) * img_crop

# Loop untuk mengambil frame
while True:
    success, img = cap.read()
    if not success:
        break

    green_background = np.zeros_like(img, dtype=np.uint8)
    green_background[:] = (255, 255, 255)

    image_resized3 = cv2.resize(bg, (img.shape[1], img.shape[0]))  # Resize bg full screen
    overlay_image_alpha(green_background, image_resized3[:, :, :3], 0, 0, image_resized3[:, :, 3] / 255.0)

    # Baca tangan
    hands, img = detector.findHands(img)
    if hands:
        hand_landmarks = hands[0]['lmList']
        if hand_landmarks:

            index_finger_x, index_finger_y = hand_landmarks[8][0], hand_landmarks[8][1]

            if rect1_position[0] < index_finger_x < rect1_position[0] + rect_size[0] and \
                    rect1_position[1] < index_finger_y < rect1_position[1] + rect_size[1]:
                rect1_position[0] = int(index_finger_x - rect_size[0] / 2)
                rect1_position[1] = int(index_finger_y - rect_size[1] / 2)

            if rect2_position[0] < index_finger_x < rect2_position[0] + rect2_size[0] and \
                    rect2_position[1] < index_finger_y < rect2_position[1] + rect2_size[1]:
                kuman1_visible = False

            if rect3_position[0] < index_finger_x < rect3_position[0] + rect3_size[0] and \
                    rect3_position[1] < index_finger_y < rect3_position[1] + rect3_size[1]:
                kuman2_visible = False

    # Overlay gambar gigi
    gigi_resized = cv2.resize(gigi, (270, 320))  # Resize gigi fixed size
    overlay_image_alpha(green_background, gigi_resized[:, :, :3], 300, 120, gigi_resized[:, :, 3] / 255.0)

    # Overlay kuman1 jika terlihat
    if kuman1_visible:
        kuman1_resized = cv2.resize(kuman1, (rect2_size[0], rect2_size[1]))  # Resize kuman1 fixed size
        overlay_image_alpha(green_background, kuman1_resized[:, :, :3], rect2_position[0], rect2_position[1], kuman1_resized[:, :, 3] / 255.0)

    # Overlay kuman2 jika terlihat
    if kuman2_visible:
        kuman2_resized = cv2.resize(kuman2, (rect3_size[0], rect3_size[1]))  # Resize kuman2 fixed size
        overlay_image_alpha(green_background, kuman2_resized[:, :, :3], rect3_position[0], rect3_position[1], kuman2_resized[:, :, 3] / 255.0)

    # Overlay pertanyaan
    pertanyaan_resized = cv2.resize(pertanyaan, (380, 140))
    overlay_image_alpha(green_background, pertanyaan_resized[:, :, :3], 135, 5, pertanyaan_resized[:, :, 3] / 255.0)

    # Overlay sikat gigi terakhir agar berada paling depan
    image_resized1 = cv2.resize(sikatGigi, (rect_size[0], rect_size[1]))
    overlay_image_alpha(green_background, image_resized1[:, :, :3], rect1_position[0], rect1_position[1], image_resized1[:, :, 3] / 255.0)

    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", green_background)

    # Keluar programnya
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Selesai
cap.release()
cv2.destroyAllWindows()
