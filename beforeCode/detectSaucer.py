import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import os
import json  # 좌표를 파일로 저장하기 위해 추가

# Load the custom YOLOv8 model with your trained weights
# Define the base directory (relative to the script's location)
base_dir = os.path.dirname(__file__)

# Define the relative path to the model file
model_path = os.path.join(base_dir, 'data', 'best.pt')

# Load YOLOv8 model using the relative path
model = YOLO(model_path)

# Camera intrinsics (replace with actual calibration data)
fx, fy = 2227.93, 2211.78  # Focal length (example values)
cx, cy = 1261.84, 2100.96       # Principal point (example values)
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0, 0, 1]])

# Configure depth and color streams from the depth camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Set confidence threshold for detections
CONFIDENCE_THRESHOLD = 0.5

try:
    while True:
        # Get both color and depth frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Perform YOLOv8 detection on the RGB frame
        results = model(color_image)

        # Extract bounding boxes and process detections
        detections = results[0].boxes
        saucer_count = 0  # "Saucer"로 탐지된 객체의 수를 셉니다
        saucer_coords = None  # "Saucer" 좌표를 저장할 변수

        for box in detections:
            conf = box.conf[0]  # Confidence
            if conf < CONFIDENCE_THRESHOLD:
                continue  # Skip detections below threshold

            x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
            class_id = box.cls[0]  # Class ID

            # 객체 이름이 "Saucer"인지 확인
            if model.names[int(class_id)] == "Saucer":
                saucer_count += 1  # "Saucer"로 탐지된 객체의 수를 증가시킴
                
                # Calculate the center of the bounding box
                x_center = int((x1 + x2) / 2)
                y_center = int((y1 + y2) / 2)

                # Get depth (z-coordinate) at the center of the detected object
                z_center = depth_frame.get_distance(x_center, y_center)

                # Saucer의 좌표를 저장
                saucer_coords = {
                    'x': x_center,
                    'y': y_center,
                    'z': z_center
                }

                # Draw bounding box and label
                cv2.rectangle(color_image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                
                # Draw class label above the bounding box
                label = f'{model.names[int(class_id)]}: {conf:.2f}'
                label_position = (int(x1), int(y1) - 10)  # Positioned above the bounding box
                cv2.putText(color_image, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Draw coordinates (x, y, z) below the bounding box
                coord_label = f'x: {x_center}, y: {y_center}, z: {z_center:.2f}m'
                coord_label_position = (int(x1), int(y2) + 20)  # Positioned below the bounding box
                cv2.putText(color_image, coord_label, coord_label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # "Saucer"가 정확히 하나만 탐지된 경우에만 JSON 파일 저장
        if saucer_count == 1 and saucer_coords is not None:
            print(f'Center coordinates: {saucer_coords}')
            
            # 좌표를 JSON 파일로 저장
            with open('coordinates.json', 'w') as coord_file:
                json.dump(saucer_coords, coord_file)

        # Display the RGB frame with detections
        cv2.imshow('Real-Time Detection with 3D Coordinates', color_image)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline
    pipeline.stop()
    cv2.destroyAllWindows()
