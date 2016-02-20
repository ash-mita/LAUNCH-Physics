#!/usr/bin/env python3

import bcrypt, sqlite3
from flask import Flask, make_response, render_template, request

app = Flask(__name__)
conn = sqlite3.connect('launch-physics.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/badges')
def badges():
    return render_template('badges.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    return 'TODO: ' + username + ':' + password

@app.route('/logout')
def logout():
    resp = make_response(render_template('redirect.html', url='/'))
    resp.headers['Location'] = '/'
    resp.status_code = 303
    resp.set_cookie('auth', value='', expires=0)
    return resp

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (' +
        'username text,' +
        'passhash text)')
    c.execute('CREATE TABLE IF NOT EXISTS badges (' +
        'username text,' +
        'name text,' +
        'date date)')

    import os

    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host=host, port=port)
