import cv2
import os

image_number = 1

latest_existing_album_number = 12
albums_to_exclude = [f'album_{i}' for i in range(1, latest_existing_album_number + 1)] + ['.DS_Store']

for album_name in os.listdir('albums'):
    if album_name not in albums_to_exclude:
        print(f'Processing {album_name}...')
        for img in os.listdir(f'albums/{album_name}/original'):
            if img != '.DS_Store':
                image = cv2.imread(f'albums/{album_name}/original/{img}')
                original = image.copy()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (3, 3), 0)
                thresh = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY_INV)[1]
                # Find contours
                cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if len(cnts) == 2 else cnts[1]
                # Iterate thorugh contours and filter for ROI
                for c in cnts:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    ROI = original[y:y+h, x:x+w]
                    cropped_img_file_name = f'albums/{album_name}/cropped/ROI_{image_number}.jpg'
                    cv2.imwrite(cropped_img_file_name, ROI)
                    file_size_mb = os.path.getsize(cropped_img_file_name) / 1024 / 1024
                    if file_size_mb < 0.05:
                        os.remove(cropped_img_file_name)
                        image_number -= 1
                    image_number += 1
print('Done.')