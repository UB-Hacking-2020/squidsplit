from bottle import route, run, static_file
import RK, stitcher

@route('/')
def index():
    return static_file("index.html", root='')

@route('/stylesheet.css')
def style():
    return static_file("stylesheet.css", root='')

@route('/request')
def spliceAndStitch(youtubeURL, text):
    RK.downloadAsMP3(youtubeURL)
    IBMjson = RK.youtubeIBManalysis(youtubeURL[-11:], "token.txt")
    RK.mp3AndTimestampsToSpliced(IBMjson, youtubeURL[-11:])
    stitcher.stringToMp3(youtubeURL[-11:], text)

run(host='localhost', port=8080, debug=True)