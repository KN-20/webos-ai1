from flask import Flask, request, jsonify

import Img_Proc as ip

app = Flask(__name__)
@app.route('/ImgRecive', methods=['GET', 'POST'])
def send_image():
    data = ip.send_food_data()
    return data

@app.route('/ImgSend', methods=['POST'])
def receive_image():
    try:
        data = request.get_json()
        print(1)
        image_data = data.get('data')
        print(2)
        img, img_path = ip.save_image(image_data)
        print(img)
        if img == 'no_data':
            print(len(img))
            return 'error'
        print(4)
        print(img_path)
        fo_na = ip.barcode_decode(img_path)

        print(5)
        print(img_path)
        allergy_date = ip.read_text(img_path)
        print(6)
        ip.food_save(fo_na, allergy_date[0], allergy_date[1])
        print(7)
        return 'success'
    except Exception as e:
        print(e)
        return 'error'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5501,debug=True)