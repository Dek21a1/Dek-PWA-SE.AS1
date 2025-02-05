from flask import Flask
from flask import render_template
from flask import request
from flask import session
import database_manager as dbHandler
import secrets

app = Flask(__name__)

app.secret_key = b'#$jgberu@$%/gibg'

app.config["SECRET_KEY"] = secrets.token_hex()
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 86400

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
            session['status'] = response
            session['mail'] = email
            session['key'] = app.config["SECRET_KEY"]
            dbHandler.update_session(email, session['key'])
            return home()
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


@app.route('/home.html', methods=['GET'])
def home():
    email = session['mail']
    user = dbHandler.get_user(email)
    id = dbHandler.get_teams(email)
    devlog = dbHandler.get_log(id)
    if not devlog:
        return render_template('/home.html', cred=session['status'], User=user, log=False)
    else:
        return render_template('/home.html', cred=session['status'], User=user, log=devlog)


@app.route('/submit_log.html', methods=['GET', 'POST'])
def submit():
    if request.method=="POST":
        log_title = request.form['title']
        log_subtitle = request.form['about']
        log_info = request.form['info']
        team = request.form['team_name']


@app.route('/sign_out')
def sign_out():
    dbHandler.reset_session(session['mail'])
    session.clear()
    return render_template('/index.html')


@app.route('/team_manage.html', methods=['GET', 'POST'])
def manage_team():
    if request.method=="POST":
        return render_template('/team_manage.html', cred=session['status'])
    else:
        id = dbHandler.perm_level(session['mail'])
        return render_template('/team_manage.html', cred=session['status'], team=id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)