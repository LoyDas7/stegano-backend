from flask import Flask, request, send_file, jsonify
from stegano import lsb
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Flask is running"

# @app.route('/encode', methods=['POST'])
# def encode():
#     if 'image' not in request.files:
#         return "No image part in the request", 400

#     image = request.files['image']
#     message = request.form.get('message')

#     if image.filename == '':
#         return "No selected file", 400

#     image_path = os.path.join(UPLOAD_FOLDER, 'input.png')
#     image.save(image_path)

#     secret = lsb.hide(image_path, message)
#     output_path = os.path.join(UPLOAD_FOLDER, 'encoded.png')
#     secret.save(output_path)

#     return send_file(output_path, mimetype='image/png')
@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files:
        return "No image part in the request", 400

    image = request.files['image']
    message = request.form.get('message')

    if image.filename == '':
        return "No selected file", 400
    if not message:
        return "No message provided", 400

    image_path = os.path.join(UPLOAD_FOLDER, 'input.png')
    output_path = os.path.join(UPLOAD_FOLDER, 'encoded.png')

    try:
        image.save(image_path)

        secret = lsb.hide(image_path, message)
        if secret is None:
            return "Failed to encode message in image", 500

        secret.save(output_path)

        if not os.path.exists(output_path):
            return "Encoded file not found", 500

        return send_file(output_path, mimetype='image/png')

    except Exception as e:
        return f"Error during encoding: {str(e)}", 500


# @app.route('/decode', methods=['POST'])
# def decode():
#     if 'image' not in request.files:
#         return "No image part in the request", 400

#     image = request.files['image']
#     image_path = os.path.join(UPLOAD_FOLDER, 'encoded.png')
#     image.save(image_path)
#     hidden_message = lsb.reveal(image_path)

#     return jsonify({'message': hidden_message})

# if __name__ == '__main__':
#     app.run(debug=True)
@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return "No image part in the request", 400

    image = request.files['image']

    if image.filename == '':
        return "No selected file", 400

    image_path = os.path.join(UPLOAD_FOLDER, 'to_decode.png')

    try:
        image.save(image_path)

        hidden_message = lsb.reveal(image_path)

        if hidden_message is None:
            return "No hidden message found in the image", 404

        return jsonify({'message': hidden_message})

    except Exception as e:
        return f"Error during decoding: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)


