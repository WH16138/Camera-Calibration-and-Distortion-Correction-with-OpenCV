import cv2
import numpy as np

img1 = cv2.imread("data/selected/frame_04.jpg")      # 원본
img2 = cv2.imread("data/output/undistorted.jpg")     # 보정 후

h = min(img1.shape[0], img2.shape[0])
img1 = cv2.resize(img1, (int(img1.shape[1] * h / img1.shape[0]), h))
img2 = cv2.resize(img2, (int(img2.shape[1] * h / img2.shape[0]), h))

combined = np.hstack((img1, img2))

cv2.putText(combined, "Original", (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
cv2.putText(combined, "Undistorted", (img1.shape[1] + 20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

cv2.imwrite("results/undistortion_comparison.jpg", combined)
print("Saved: results/undistortion_comparison.jpg")