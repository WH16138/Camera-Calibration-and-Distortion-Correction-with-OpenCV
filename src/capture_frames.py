import cv2
import os

video_path = "data/raw/checkboard.mp4"
output_dir = "data/selected"
frame_interval = 15  # 저장 간격 프레임

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit()

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_interval == 0:
        filename = os.path.join(output_dir, f"frame_{saved_count:02d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        saved_count += 1

    frame_count += 1

cap.release()
print(f"Done. Saved {saved_count} frames.")