import subprocess
import torch.cuda

print(torch.cuda.is_available())
command = "yolo task=detect mode=train model=yolov8l.pt data=C:/Users/pwlno/Desktop/v3/data.yaml epochs=45 imgsz=640 " \
          "batch=8 mosaic=0"
subprocess.run(command, shell=True)

