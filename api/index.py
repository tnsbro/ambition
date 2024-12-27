from flask import Flask, request, render_template, redirect, url_for, make_response, send_from_directory
from pymongo import MongoClient
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 비밀 키 설정

client = MongoClient("mongodb+srv://ambition:ambition@cluster0.oycph.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") 
db = client['ambition']
members_collection = db['members']

serializer = URLSafeTimedSerializer(app.secret_key)

@app.route('/')
def index():
    email_cookie = request.cookies.get('email')
    if email_cookie:
        try:
            email = serializer.loads(email_cookie, max_age=60*60*24*30)  # 쿠키 유효기간 30일
            member = members_collection.find_one({'email': email})
            if member:
                return render_template('mypage.html', member=member)
        except:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/find')
def find_choice():
    return render_template('choice.html')

@app.route('/map/<tag>')
def map(tag):
    return render_template('map.html', tag=tag)

@app.route('/stampimg')
def stampimg():
    return send_from_directory('static', 'stamp.png')

@app.route('/mypage')
def mypage():
    email_cookie = request.cookies.get('email')
    if email_cookie:
        try:
            email = serializer.loads(email_cookie, max_age=60*60*24*30)  # 쿠키 유효기간 30일
            member = members_collection.find_one({'email': email})
            if member:
                if 'stamp' not in member:
                    member['stamp'] = 0
                return render_template('mypage.html', member=member)
        except:
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        member = members_collection.find_one({'email': request.form['email']})
        if member and member['password'] == request.form['password']:
            response = make_response(redirect(url_for('mypage')))
            email_cookie = serializer.dumps(request.form['email'])
            response.set_cookie('email', email_cookie, max_age=60*60*24*30)  # 쿠키 유효기간 30일
            return response
        return render_template('login.html', error=401)
    return render_template('login.html')

@app.route('/join', methods=['POST', 'GET'])
def join():
    if request.method == 'POST':
        member = members_collection.find_one({'email': request.form['email']})
        if member:
            return render_template('join.html', error=409)
        member_info = {
            'email': request.form['email'],
            'password': request.form['password'],
            'name': request.form['username'],
            'stamp' : 0
        }
        members_collection.insert_one(member_info)
        return redirect(url_for('login'))
    return render_template('join.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('email')
    return response

if __name__ == '__main__':
    app.run(debug=True)