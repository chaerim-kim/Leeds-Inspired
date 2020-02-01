from flask import Flask, jsonify
from flask_restful import Api
import json


app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def category_json():

    # opens json file for category
    with open('category.json') as json_file:
        data = json.load(json_file)

    return jsonify(data)


if __name__ == '__main__':
    app.run(port=1111, debug=True)
