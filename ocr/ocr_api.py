from flask import Flask, request, abort, jsonify, make_response, json
from main import run

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def process_image():
    response = dict(request.json)
    images = list(response['images'])
    if len(images) == 0:
        return jsonify({'status':'Bad request','code':400,'message':'Pas d\'images passes en parametres'})
    result = run(images)
    if not result:
        return jsonify({'status':'Not found','code':404,'message':'Les images passes en parametres sont introuvables'})
    return jsonify({'status':'OK','code':200,'message':'Les images ont ete bien traite','result':result})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)