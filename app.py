from flask import Flask, render_template, request, session, redirect, url_for, make_response
from dotenv import load_dotenv
import json

import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
print(script_directory)

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# python -c 'import secrets; print(secrets.token_hex(32))'
# bb7c4c42c5dd2f2994e925e1e21eb550337e1878f8542ee6d8e454e707da0cfb
# export SECRET_KEY='bb7c4c42c5dd2f2994e925e1e21eb550337e1878f8542ee6d8e454e707da0cfb'

app.secret_key = os.getenv('SECRET_KEY')


@app.route('/index')
def index():
    if "username" in session:
        cookie = request.cookies.get('username')
        return render_template('index.html', username = session['username'], cookie = cookie)
        
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('username')
    return resp

@app.route('/signup', methods= ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeatPassword = request.form['repeatpass']
        if password == repeatPassword:
            user = {
                'username': username,
                'email': email,
                'password': password
            }
            try:
                with open(f"{script_directory}/static/newUser.txt", "r+") as file:
                    allUsers = json.loads(file.read())

                    if allUsers and type(allUsers) == dict:
                        allUsers.update({email: user})
                        file.seek(0)
                    else:
                        allUsers = {}
                        allUsers.update({email: user})
                    file.write(json.dumps(allUsers,indent=2))
            except Exception as e:
                print("in except clause", e)
                allUsers = {}
                allUsers.update({email: user})
                with open(f"{script_directory}/static/newUser.txt", "w") as file:
                    file.write(json.dumps(allUsers,indent=2))

            # return render_template('login.html')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods= ['post', 'get'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with open(f"{script_directory}/static/newUser.txt", "r") as file:
            allUsers = json.loads(file.read())
        if email in allUsers:
            if allUsers[email]["password"] == password:
                username = allUsers[email]["username"]
                session['username'] = username
                # return render_template('index.html', username = username)
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', session['username'])
                return resp
            
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug= True)