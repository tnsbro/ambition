from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/find')
def find_choice():
    return render_template('choice.html')

@app.route('/map/<tag>')
def map(tag):
    return render_template('map.html', tag=tag)

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/join', methods=['POST', 'GET'])
def join():
    return render_template('join.html')


if __name__ == '__main__':
    app.run(debug=True)