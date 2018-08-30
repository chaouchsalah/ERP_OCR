from flask import Flask, request, abort, jsonify, make_response, json
from main import run

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def process_image():
    response = dict(request.json)
    images = list(response['images'])
    if len(images) == 0:
        return jsonify({'success':False,'message':'No images were found'})
    return jsonify({'success':True,'message':'Images processed successfully','result':run(images)})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)