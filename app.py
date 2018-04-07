from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
from flask_cors import CORS
from snownlp import SnowNLP
from sklearn.externals import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
cors = CORS(app, resources={r"/predict": {"origins": "*"}})
api = Api(app)

# 读取模型
restaurant_clf = joblib.load('./models/restaurant_comment.pkl')
douban_clf = joblib.load('./models/douban_comment.pkl')

# 参数解析
parser = reqparse.RequestParser()
parser.add_argument('sentence', type=str)
parser.add_argument('type', type=str)

class Prediction(Resource):
    def post(self):
        args = parser.parse_args()
        if args['type'] == 'restaurant':
            result = restaurant_clf.predict([args['sentence']]).astype(np.str)
            return result[0], 200
        elif args['type'] == 'douban':
            result = douban_clf.predict([args['sentence']]).astype(np.str)
            return result[0], 200
        else:
            s = SnowNLP(args['sentence'])
            return s.sentiments*5, 200

api.add_resource(Prediction, '/predict')

if __name__ == '__main__':
    app.run(debug=True)
