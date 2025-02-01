from flask import Flask
from flask import render_template
from flask import request
import database_manager as dbHandler

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    return render_template('/index.html')

@app.route('/login.html', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email = request.form['eml']
        password = request.form['pswrd']
        response = dbHandler.retrieve_details(email, password)
        if response == True:
            return render_template('/home.html')
        else:
            return render_template('/login.html')
    else:
        return render_template('/login.html')


@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['usrnm']
        email = request.form['eml']
        password = request.form['pswrd']
        status = dbHandler.insert_details(username, email, password)
        if status == True:
            return render_template('/login.html')
        else:
            print(status)
    else:
        return render_template('/signup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)