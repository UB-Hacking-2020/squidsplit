from flask import Flask, request, send_from_directory
import json
import RK, stitcher
from flask_cors import CORS

app = Flask('squidsplit')
CORS(app)


@app.route('/request', methods=['POST'])
def spliceAndStitch():
    inputJSON = request.get_data()
    wossname = json.loads(inputJSON)
    url = wossname["url"]
    text = wossname["text"].lower()
    if not text.endswith("."):
        text += "."
    RK.completeSlicer(url)
    resp = Flask.make_response(app, stitcher.stringToMp3(url[-11:], text))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.route('/data/output/<path:path>')
def output(path):
    return send_from_directory('data/output/', path)