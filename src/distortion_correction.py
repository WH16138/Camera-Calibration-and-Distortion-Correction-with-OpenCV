import cv2
import numpy as np
import os

# ===== 직접 입력: calibration 결과값 =====
camera_matrix = np.array([
    [970.199798, 0.0, 554.873799],
    [0.0, 963.270873, 950.035093],
    [0.0, 0.0, 1.0]
], dtype=np.float32)

dist_coeffs = np.array([
    [-0.020841, 0.088206, -0.009084, 0.007036, -0.068789]
], dtype=np.float32)

# ===== 입력 / 출력 경로 =====
input_image_path = "data/selected/frame_63.jpg"
output_dir = "data/output"
os.makedirs(output_dir, exist_ok=True)

# ===== 이미지 읽기 =====
img = cv2.imread(input_image_path)
if img is None:
    print("Error: Cannot load image.")
    exit()

h, w = img.shape[:2]

# ===== 최적 새 카메라 행렬 계산 =====
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix, dist_coeffs, (w, h), 1, (w, h)
)

# ===== 왜곡 보정 =====
undistorted = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# ===== ROI crop (선택) =====
x, y, w_roi, h_roi = roi
if w_roi > 0 and h_roi > 0:
    undistorted_cropped = undistorted[y:y+h_roi, x:x+w_roi]
else:
    undistorted_cropped = undistorted

# ===== 저장 =====
cv2.imwrite(os.path.join(output_dir, "undistorted.jpg"), undistorted)
cv2.imwrite(os.path.join(output_dir, "undistorted_cropped.jpg"), undistorted_cropped)

# ===== 비교 출력 =====
cv2.imshow("Original", img)
cv2.imshow("Undistorted", undistorted)
cv2.imshow("Undistorted Cropped", undistorted_cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("Saved:")
print(" - data/output/undistorted.jpg")
print(" - data/output/undistorted_cropped.jpg")