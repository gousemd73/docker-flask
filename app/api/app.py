from flask import Flask, jsonify, request
from utilities import predict_pipeline
from pymongo import MongoClient


app = Flask(__name__)

# client = MongoClient('mongodb://admin:password@localhost:27017/') # mongodb://username:password@porthostingapplication of mongo
client = MongoClient('mongodb://admin:password@mongoDB:27017/')

db     = client['sentiment_db']
output = db['predictions']


@app.post('/predict')
def predict():
    data = request.json
    try:
        sample = data['text']
    except KeyError:
        return jsonify({'error': 'No text sent'})

    # sample = [sample]

    predictions = predict_pipeline(sample)
    try:
        result = jsonify(predictions)
        output.insert_many(predictions)
    except TypeError as e:
        result = jsonify({'error': str(e)})
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)