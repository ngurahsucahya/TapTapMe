import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def main():
    # Buka kamera, biasanya 0 untuk webcam
    cap = cv2.VideoCapture(0)

    # sikatGigi, sebenarnya bentuknya kotak
    rect1_position = [190, 250]
    rect_size = [290, 290]

    # kuman1
    rect2_position = [300, 110]
    rect2_size = [60, 80]
    kuman1_visible = True  # Visibility flag for kuman1

    # kuman2
    rect3_position = [400, 130]
    rect3_size = [60, 80]
    kuman2_visible = True  # Visibility flag for kuman2

    # kuman3
    rect4_position = [440, 90]
    rect4_size = [60, 80]
    kuman3_visible = True  # Visibility flag for kuman2

    # kuman4
    rect5_position = [250, 220]
    rect5_size = [60, 80]
    kuman4_visible = True  # Visibility flag for kuman2

    # kuman5
    rect6_position = [350, 210] #horizontal, vertikal
    rect6_size = [60, 80]
    kuman5_visible = True  # Visibility flag for kuman2

    # kuman6
    rect7_position = [200, 110] #horizontal, vertikal
    rect7_size = [60, 80]
    kuman6_visible = True  # Visibility flag for kuman2

    sikatGigi = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Sikat gigi.png", cv2.IMREAD_UNCHANGED)
    kuman1 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
    kuman2 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
    kuman3 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
    kuman4 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
    kuman5 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
    kuman6 = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Kuman.png", cv2.IMREAD_UNCHANGED)
    bg = cv2.imread("../src/images/mainMenu/BG - Step 4 sehat.png", cv2.IMREAD_UNCHANGED)

    gigi = cv2.imread("../src/images/Sahabat sehat -20240518T025648Z-001/Sahabat sehat/Gigi.png", cv2.IMREAD_UNCHANGED)

    # pertanyaan = cv2.imread("../src/images/Ambil 1 bola.png", cv2.IMREAD_UNCHANGED)

    selamat = cv2.imread("../src/images/Logo.png", cv2.IMREAD_UNCHANGED)  # Load congratulatory image

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

                if rect4_position[0] < index_finger_x < rect4_position[0] + rect4_size[0] and \
                        rect4_position[1] < index_finger_y < rect4_position[1] + rect4_size[1]:
                    kuman3_visible = False

                if rect5_position[0] < index_finger_x < rect5_position[0] + rect5_size[0] and \
                        rect5_position[1] < index_finger_y < rect5_position[1] + rect5_size[1]:
                    kuman4_visible = False

                if rect6_position[0] < index_finger_x < rect6_position[0] + rect6_size[0] and \
                        rect6_position[1] < index_finger_y < rect6_position[1] + rect6_size[1]:
                    kuman5_visible = False

                if rect7_position[0] < index_finger_x < rect7_position[0] + rect7_size[0] and \
                        rect7_position[1] < index_finger_y < rect7_position[1] + rect7_size[1]:
                    kuman6_visible = False

        # Overlay gambar gigi
        gigi_resized = cv2.resize(gigi, (370, 300))  # Resize gigi fixed size
        overlay_image_alpha(green_background, gigi_resized[:, :, :3], 150,20, gigi_resized[:, :, 3] / 255.0)

        # Overlay kuman1 jika terlihat
        if kuman1_visible:
            kuman1_resized = cv2.resize(kuman1, (rect2_size[0], rect2_size[1]))  # Resize kuman1 fixed size
            overlay_image_alpha(green_background, kuman1_resized[:, :, :3], rect2_position[0], rect2_position[1], kuman1_resized[:, :, 3] / 255.0)

        # Overlay kuman2 jika terlihat
        if kuman2_visible:
            kuman2_resized = cv2.resize(kuman2, (rect3_size[0], rect3_size[1]))  # Resize kuman2 fixed size
            overlay_image_alpha(green_background, kuman2_resized[:, :, :3], rect3_position[0], rect3_position[1], kuman2_resized[:, :, 3] / 255.0)

        # Overlay kuman2 jika terlihat
        if kuman3_visible:
            kuman3_resized = cv2.resize(kuman3, (rect4_size[0], rect4_size[1]))  # Resize kuman2 fixed size
            overlay_image_alpha(green_background, kuman3_resized[:, :, :3], rect4_position[0], rect4_position[1], kuman3_resized[:, :, 3] / 255.0)

        # Overlay kuman2 jika terlihat
        if kuman4_visible:
            kuman4_resized = cv2.resize(kuman4, (rect5_size[0], rect5_size[1]))  # Resize kuman2 fixed size
            overlay_image_alpha(green_background, kuman4_resized[:, :, :3], rect5_position[0], rect5_position[1], kuman4_resized[:, :, 3] / 255.0)

        # Overlay kuman2 jika terlihat
        if kuman5_visible:
            kuman5_resized = cv2.resize(kuman5, (rect6_size[0], rect6_size[1]))  # Resize kuman2 fixed size
            overlay_image_alpha(green_background, kuman5_resized[:, :, :3], rect6_position[0], rect6_position[1], kuman5_resized[:, :, 3] / 255.0)

        # Overlay kuman2 jika terlihat
        if kuman6_visible:
            kuman6_resized = cv2.resize(kuman6, (rect7_size[0], rect7_size[1]))  # Resize kuman2 fixed size
            overlay_image_alpha(green_background, kuman6_resized[:, :, :3], rect7_position[0], rect7_position[1], kuman6_resized[:, :, 3] / 255.0)

        # # Overlay pertanyaan
        # pertanyaan_resized = cv2.resize(pertanyaan, (380, 140))
        # overlay_image_alpha(green_background, pertanyaan_resized[:, :, :3], 135, 5, pertanyaan_resized[:, :, 3] / 255.0)

        # Overlay sikat gigi terakhir agar berada di paling depan
        image_resized1 = cv2.resize(sikatGigi, (rect_size[0], rect_size[1]))
        overlay_image_alpha(green_background, image_resized1[:, :, :3], rect1_position[0], rect1_position[1],
                            image_resized1[:, :, 3] / 255.0)
        # Check if all germs are gone
        if not kuman1_visible and not kuman2_visible and not kuman3_visible and not kuman4_visible and not kuman5_visible and not kuman6_visible:
            selamat_resized = cv2.resize(selamat, (300, 150))  # Resize congratulatory image
            overlay_image_alpha(green_background, selamat_resized[:, :, :3], (img.shape[1] - 300) // 2, (img.shape[0] - 150) // 2, selamat_resized[:, :, 3] / 255.0)



        cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Image", green_background)

        # keluar programnya atau restart
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('a'):
            cap.release()
            cv2.destroyAllWindows()
            main()
            return

        # selesai
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
