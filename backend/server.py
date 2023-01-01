from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from utils import process_tokens, beam_search
from model import Encoder, Decoder
import torch

# current datast: Flickr8k
CAPTION_PATH = './datasets/Flickr8k/captions.txt'
ENCODER_PATH = './weights/encoder.pth'
DECODER_PATH = './weights/decoder.pth'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = Flask(__name__)
api = Api(app)

# get tokens corresponding to dataset model was trained on
tokens, tokens_to_id, num_tokens = process_tokens(CAPTION_PATH)

# instantiate model with trained weights
encoder = Encoder().to(DEVICE)
decoder = Decoder(
    decoder_dim=256,
    attention_dim=256,
    num_tokens=num_tokens,
    embed_size=300,
    device=DEVICE
).to(DEVICE)

encoder.load_state_dict(torch.load(ENCODER_PATH, map_location=DEVICE))
decoder.load_state_dict(torch.load(DECODER_PATH, map_location=DEVICE))

encoder.eval()
decoder.eval()

# storing captions as a mock database
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
        caption = beam_search(encoder, decoder, filepath, tokens, tokens_to_id, num_tokens)

        caption_id = int(max(CAPTIONS.keys()).strip('caption')) + 1
        caption_id = 'caption%i' % caption_id
        CAPTIONS[caption_id] = caption
        return jsonify(CAPTIONS[caption_id])


api.add_resource(CaptionList, '/caption')


if __name__ == '__main__':
    app.run(debug=True)

