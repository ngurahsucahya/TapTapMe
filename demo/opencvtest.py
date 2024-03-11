import cv2

def main():
    # Buka webcam
    cap = cv2.VideoCapture(0)

    # Periksa apakah webcam terbuka dengan benar
    if not cap.isOpened():
        print("Tidak dapat membuka webcam")
        return

    while True:
        # Baca frame dari webcam
        ret, frame = cap.read()

        # Periksa apakah frame berhasil dibaca
        if not ret:
            print("Tidak dapat membaca frame")
            break

        # Tampilkan frame
        cv2.imshow("Webcam", frame)

        # Tunggu 1ms dan periksa tombol keyboard
        key = cv2.waitKey(1)
        if key == ord('q'):  # Tekan 'q' untuk keluar
            break

    # Tutup webcam dan jendela tampilan
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
