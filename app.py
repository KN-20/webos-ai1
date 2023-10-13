from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import cv2
import time
import base64
import numpy as np

global model
model = YOLO('hbest.pt')

app = Flask(__name__)

@app.route('/timeout', methods=['POST'])
def timeout():
    time.sleep(120)
    return 0

@app.route('/ImgSend', methods=['POST'])
def receive_image():
    try:
        data = request.get_json()
        image_data = data.get('data')
        img = save_image(image_data)
        if len(img) < 1:
            return jsonify({'status': 'error'})
        image = yolo_image(img)
        return jsonify({'status': 'success', 'food': '마가렛트', 'allergy':['우유', '밀'], 'date':'2024-01-01', 'data': str(image)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def save_image(encoded_image):
    try:
        print(1)
        image_data = BytesIO(bytes(encoded_image, 'utf-8'))
        print(2)
        image = Image.open(BytesIO(base64.b64decode(encoded_image)))
        image = np.array(image)
        return image
    except Exception as e:
        print(f"Error saving image: {e}")
        return

def yolo_image(image):
    res = model.predict(source=image)
    return res
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5501)
