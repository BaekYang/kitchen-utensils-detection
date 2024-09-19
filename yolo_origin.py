from ultralytics import YOLO

# Load YOLOv8 model (for example, Nano model for faster training)
model = YOLO('yolov8n.yaml')

# Train the model on the custom dataset and save the weights to a custom directory
model.train(data='/home/piai/ddolmang/dataset.yaml', epochs=100, imgsz=640, 
            project='/home/piai/ddolmang/model1/yolov8n_custom.pt', name='my_custom_model')
