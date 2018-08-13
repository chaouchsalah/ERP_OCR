from flask import Flask, request, abort, jsonify, make_response
from main import run

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ocr/process', methods=['POST'])
def create_task():
    if not request.json or not 'id' in request.json:
        abort(400)
    images = []
    for image in request.json['images']:
        new_image = {
            'id': image['id'],
            'name': image['name']
        }
        images.append(new_image)
    """if run(images) is not None:
        return jsonify({'images': images}), 201"""

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)