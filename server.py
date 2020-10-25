from bottle import route, run, static_file
import RK

@route('/')
def index():
    return static_file("index.html", root='')

@route('/stylesheet.css')
def style():
    return static_file("stylesheet.css", root='')

@route('/splicer')
def splice(youtubeURL):
    RK.downloadAsMP3(youtubeURL)
    IBMjson = RK.youtubeIBManalysis(youtubeURL[-11:])
    RK.mp3AndTimestampsToSpliced(IBMjson, youtubeURL[-11:])

run(host='localhost', port=8080, debug=True)