from bottle import route, run, static_file
import json
import RK, stitcher

@route('/')
def index():
    return static_file("index.html", root='')

@route('/stylesheet.css')
def style():
    return static_file("stylesheet.css", root='')

@route('/request')
def spliceAndStitch(inputJSON):
    wossname = json.loads(inputJSON)
    url = wossname["url"]
    text = wossname["text"]
    RK.downloadAsMP3(url)
    IBMjson = RK.youtubeIBManalysis(url[-11:], "token.txt")
    RK.mp3AndTimestampsToSpliced(IBMjson, url[-11:])
    return "data/output/" + stitcher.stringToMp3(url[-11:], text)

run(host='localhost', port=8080, debug=True)