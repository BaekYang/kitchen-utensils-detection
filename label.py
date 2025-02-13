import os
import json
from PIL import Image  # 이미지 크기를 자동으로 얻기 위해 사용

def convert_coco_to_yolo(json_file, img_file, output_dir):
    # 이미지 크기를 자동으로 불러오기
    with Image.open(img_file) as img:
        img_width, img_height = img.size

    # JSON 파일을 읽어들임
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 출력 디렉토리 생성 (없으면 생성)
    os.makedirs(output_dir, exist_ok=True)

    # 이미지에 대한 어노테이션 정보 변환
    for annotation in data['annotations']:
        # 이미지 파일 이름을 그대로 사용
        img_file_name = os.path.splitext(os.path.basename(img_file))[0] + ".txt"
        bbox = annotation['bbox']

        # 클래스 ID를 강제로 0으로 변경 (YOLOv8에서 클래스 ID는 0부터 시작해야 함)
        class_id = 0

        # 바운딩 박스 정보 (YOLO 형식으로 변환)
        x, y, w, h = bbox
        x_center = (x + w / 2) / img_width
        y_center = (y + h / 2) / img_height
        w /= img_width
        h /= img_height

        # 변환된 바운딩 박스 정보를 YOLO 형식으로 파일에 저장
        label_path = os.path.join(output_dir, img_file_name)
        with open(label_path, 'w') as label_file:
            label_file.write(f"{class_id} {x_center} {y_center} {w} {h}\n")

base_dir = os.path.dirname(os.path.abspath(__file__))

# 데이터셋 경로 설정
train_images_dir = os.path.join(base_dir, 'data/train/images')
train_labels_dir = os.path.join(base_dir, 'data/train/labels')
val_images_dir = os.path.join(base_dir, 'data/val/images')
val_labels_dir = os.path.join(base_dir, 'data/val/labels')

# 모든 train 이미지와 JSON 파일을 변환하여 라벨 생성
for img_file in os.listdir(train_images_dir):
    if img_file.endswith('.png'):  # 이미지 파일에 대해서만 처리
        json_file = img_file.replace('.png', '.json')  # JSON 파일 이름 유추
        json_path = os.path.join(train_images_dir, json_file)
        img_path = os.path.join(train_images_dir, img_file)

        # JSON 파일이 있는지 확인 후 라벨 변환
        if os.path.exists(json_path):
            convert_coco_to_yolo(json_path, img_path, train_labels_dir)

# 모든 val 이미지와 JSON 파일을 변환하여 라벨 생성
for img_file in os.listdir(val_images_dir):
    if img_file.endswith('.png'):  # 이미지 파일에 대해서만 처리
        json_file = img_file.replace('.png', '.json')  # JSON 파일 이름 유추
        json_path = os.path.join(val_images_dir, json_file)
        img_path = os.path.join(val_images_dir, img_file)

        # JSON 파일이 있는지 확인 후 라벨 변환
        if os.path.exists(json_path):
            convert_coco_to_yolo(json_path, img_path, val_labels_dir)
