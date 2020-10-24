from bottle import route, run, static_file

@route('/')
def index():
    return static_file("index.html", root='')

@route('/stylesheet.css')
def style():
    return static_file("stylesheet.css", root='')

run(host='localhost', port=8080, debug=True)