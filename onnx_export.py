from ultralytics import YOLO

model = YOLO('card_recognition.pt')
model.export(format="onnx")