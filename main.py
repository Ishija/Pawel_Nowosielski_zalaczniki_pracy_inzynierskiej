import tensorflow as tf
import cv2
import math
import cvzone
import time
from ultralytics import YOLO
from cards_list import cards_model, combinations
import numpy as np

classNames = ['10C', '10D', '10H', '10S', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C',
              '7D', '7H', '7S', '8C', '8D', '8H', '8S', '9C', '9D', '9H', '9S', 'AC', 'AD',
              'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']

card_recognition_model = YOLO("card_recognition.pt")
cap = cv2.VideoCapture(0)
cap.set(3, 1240)
cap.set(4, 720)
set_prediction_model = tf.keras.models.load_model('prediction_model_2_500e.h5')
cards_in_game = []


def add_to_cards(card):
    if card not in cards_in_game:
        cards_in_game.append(card)


while True:
    success, img = cap.read()
    results = card_recognition_model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            conf = math.ceil((box.conf[0] * 100))
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)),
                               scale=1, thickness=1, colorR=(0, 0, 0), colorT=(255, 255, 255))
            if conf > 85:
                if classNames[cls] == '10D':
                    add_to_cards('TD')
                elif classNames[cls] == '10S':
                    add_to_cards('TS')
                elif classNames[cls] == '10C':
                    add_to_cards('TC')
                elif classNames[cls] == '10H':
                    add_to_cards('TH')
                else:
                    add_to_cards(classNames[cls])

        print(cards_in_game)

        if len(cards_in_game) == 16:
            cards_numbers = [cards_model[k] for k in cards_in_game]
            result = set_prediction_model.predict(np.array([cards_numbers]))
            best_set = np.argmax(result)
            print(f'Best winning set: {combinations[best_set]}')
            time.sleep(10)
            cards_in_game.clear()

    cv2.imshow("Camera", img)
    cv2.waitKey(1)
