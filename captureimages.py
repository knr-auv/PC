"""Program działa z Windowsem, przetestowany. Z linuxem należałoby sprawdzić ścieżki. Sprawdzić numer kamery 31line"""
import os
import time

import cv2

# Tworzenie folderu na outputy z programu, jezeli nie istnieje
fileDir = os.path.dirname(os.path.realpath('__file__'))
if not os.path.isdir(os.path.join(fileDir, "capturedimages")):
    os.mkdir(os.path.join(fileDir, "capturedimages"))

# Sprawdzanie, czy jest już utworzony folder dla danej sesji programu, żeby nie nadpisywać starych
check_counter = 0
while True:
    output_dir = os.path.join(fileDir, "capturedimages/capturedimages_{}".format(check_counter))
    if os.path.isdir(output_dir):
        check_counter += 1
    else:
        os.mkdir(output_dir)
        break

# Wybieranie trybu
print("Wybierz tryb dzialania programu:\n"
      "1: Spacja powoduje utworzenie obrazu\n"
      "2: Zdjecia robia sie z zadana czestotliwoscia")
mode = int(input())
if mode == 2:
    print("Podaj czestotliwosc robienia zdjec w Hz (zalecane 5 - 20)")
    frequency = int(input())

# Numer kamery podlaczonej do komputera moze musiec byc zmieniony, jezeli jest wiecej niz jedna kamera
cam = cv2.VideoCapture(cv2.CAP_DSHOW+1)
cam.set(3, 1920)
cam.set(4, 1080)
cv2.namedWindow("capturedimages")

# Pobieranie obrazu z kamery
img_counter = 0
while True:
    ret, frame = cam.read()
    cv2.imshow("capturedimages", frame)
    if not ret:
        break
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC
        print("Escape, zamykanie")
        break
    elif mode == 2:
        img_name = "{}.png".format(img_counter)
        cv2.imwrite(os.path.join(output_dir, img_name), frame)
        print("{} zapisano!".format(img_name))
        img_counter += 1
        time.sleep(1/frequency)
    elif mode == 1 and k%256 == 32:
        # SPACE
        img_name = "{}.png".format(img_counter)
        cv2.imwrite(os.path.join(output_dir, img_name), frame)
        print("{} zapisano!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()