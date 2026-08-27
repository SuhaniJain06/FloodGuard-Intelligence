import cv2

from feature2_detector import detect_people


# ============================================================
# RUN FEATURE 2 TEST
# ============================================================

image_path = "test_img2.jpg"

output, detections, count = detect_people(
    image_path
)


print()
print("=" * 60)
print("FEATURE 2 TEST")
print("=" * 60)

print("👥 People detected:", count)
print("📦 Bounding boxes:", len(detections))


for i, detection in enumerate(
    detections,
    start=1
):

    x1, y1, x2, y2, score = detection

    print(
        f"Person {i}: "
        f"confidence={score:.3f}, "
        f"bbox={[x1, y1, x2, y2]}"
    )


# ============================================================
# SAVE RESULT
# ============================================================

cv2.imwrite(
    "feature2_detection_result.png",
    output
)

print()
print("✅ Saved: feature2_detection_result.png")