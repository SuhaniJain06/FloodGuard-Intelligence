import cv2
import torch
from ultralytics import YOLO
from torchvision.ops import nms


MODEL_PATH = "floodguard_person_v2.pt"

model = YOLO(MODEL_PATH)

DEVICE = 0 if torch.cuda.is_available() else "cpu"

print("✅ Feature 2 model loaded")
print("Device:", "GPU" if DEVICE == 0 else "CPU")


def detect_people(
    image_path,
    tile_size=512,
    overlap=0.25,
    confidence=0.15,
    nms_iou=0.35,
    min_box_area=20
):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    height, width = image.shape[:2]

    stride = int(tile_size * (1 - overlap))

    detections = []

    for y in range(0, height, stride):

        for x in range(0, width, stride):

            x2 = min(x + tile_size, width)
            y2 = min(y + tile_size, height)

            x1 = max(0, x2 - tile_size)
            y1 = max(0, y2 - tile_size)

            tile = image[y1:y2, x1:x2]

            results = model.predict(
                source=tile,
                conf=confidence,
                imgsz=640,
                device=DEVICE,
                verbose=False
            )

            result = results[0]

            if result.boxes is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            scores = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()

            for box, score, cls in zip(
                boxes,
                scores,
                classes
            ):

                # Class 0 = person
                if int(cls) != 0:
                    continue

                bx1, by1, bx2, by2 = box

                bx1 += x1
                bx2 += x1
                by1 += y1
                by2 += y1

                area = (
                    (bx2 - bx1) *
                    (by2 - by1)
                )

                if area < min_box_area:
                    continue

                detections.append([
                    float(bx1),
                    float(by1),
                    float(bx2),
                    float(by2),
                    float(score)
                ])

    if len(detections) == 0:
        return image, [], 0

    boxes = torch.tensor(
        [d[:4] for d in detections],
        dtype=torch.float32
    )

    scores = torch.tensor(
        [d[4] for d in detections],
        dtype=torch.float32
    )

    keep = nms(
        boxes,
        scores,
        nms_iou
    ).tolist()

    final_detections = [
        detections[i]
        for i in keep
    ]

    output = image.copy()

    for i, detection in enumerate(
        final_detections,
        start=1
    ):

        x1, y1, x2, y2, score = detection

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        cv2.putText(
            output,
            f"Person {i} ({score:.2f})",
            (x1, max(20, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2
        )

    return (
        output,
        final_detections,
        len(final_detections)
    )