import cv2
import numpy as np
import os
import glob

# ===== 설정 =====
board_pattern = (10, 7)      # 내부 코너 수
board_cellsize = 25.0        # mm
image_dir = "data/selected"
result_dir = "results"

os.makedirs(result_dir, exist_ok=True)

# ===== 코너 정밀화 조건 =====
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# ===== 3D 기준 좌표 생성 =====
objp = np.zeros((board_pattern[0] * board_pattern[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:board_pattern[0], 0:board_pattern[1]].T.reshape(-1, 2)
objp *= board_cellsize

# ===== 저장용 =====
objpoints = []   # 3D points
imgpoints = []   # 2D points

images = glob.glob(os.path.join(image_dir, "*.jpg"))

success_count = 0

for idx, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, board_pattern, None)

    if ret:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        cv2.drawChessboardCorners(img, board_pattern, corners2, ret)

        save_path = os.path.join(result_dir, f"detected_{idx:02d}.jpg")
        cv2.imwrite(save_path, img)

        print(f"[OK] {fname}")
        success_count += 1
    else:
        print(f"[FAIL] {fname}")

print(f"\nDetected corners in {success_count} / {len(images)} images.")

if success_count < 3:
    print("Not enough valid images for calibration.")
    exit()

# 마지막으로 읽은 gray의 shape 사용
image_size = gray.shape[::-1]

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    image_size,
    None,
    None
)

print("\n=== Calibration Result ===")
print("RMS Reprojection Error:", ret)
print("\nCamera Matrix:")
print(camera_matrix)
print("\nDistortion Coefficients:")
print(dist_coeffs)

# 결과 저장
with open("results/calibration_result.txt", "w", encoding="utf-8") as f:
    f.write("=== Calibration Result ===\n")
    f.write(f"RMS Reprojection Error: {ret}\n\n")
    f.write("Camera Matrix:\n")
    f.write(np.array2string(camera_matrix, precision=6))
    f.write("\n\nDistortion Coefficients:\n")
    f.write(np.array2string(dist_coeffs, precision=6))
    f.write("\n")