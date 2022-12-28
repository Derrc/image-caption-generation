from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# storing captions just for practice
CAPTIONS = {
    'caption1': 'Initial Caption'
}

parser = reqparse.RequestParser()
parser.add_argument("source")

class CaptionList(Resource):

    # return all captions
    def get(self):
        return jsonify(CAPTIONS)

    # gets the image source and run inference -> add caption to CAPTIONS
    def post(self):
        args = parser.parse_args(strict=True)
        filepath = args['source']
        # run inference here
        caption_id = int(max(CAPTIONS.keys()).strip('caption')) + 1
        caption_id = 'caption%i' % caption_id
        CAPTIONS[caption_id] = filepath
        return jsonify(CAPTIONS[caption_id])


api.add_resource(CaptionList, '/caption')


if __name__ == '__main__':
    app.run(debug=True)

