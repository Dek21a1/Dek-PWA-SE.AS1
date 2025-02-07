from flask import Flask
from flask import render_template
from flask import request
from flask import session
import database_manager as dbHandler
import secrets

app = Flask(__name__)


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
            session['logs'] = False
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
        devlog = session['logs']
        user = dbHandler.get_user(email)
        id = dbHandler.get_teams(email)
        return render_template('/home.html', cred=session['status'], User=user, teams=id, log=devlog)


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
    
@app.route('/accept_team.html', methods=['POST'])
def accept_team():
    if request.method=="POST":
        team = request.form['name']
        invite = request.form['role']
        user = session['mail']
        if invite == 'request':
            dbHandler.accept_team(team, user)
            return manage_team()
    
@app.route('/invite_user.html', methods=['POST'])
def invite_user():
    if request.method=="POST":
        name = request.form['team']
        invite = request.form['user']
        clearance = 'request'
        dbHandler.create_team(name, invite, clearance)
        return manage_team()

@app.route('/create_team.html', methods=['POST'])
def create_team():
    if request.method=="POST":
        team = request.form['name']
        user = session['mail']
        clearance = 'manager'
        dbHandler.create_team(team, user, clearance)
        return manage_team()
    
@app.route('/view_log.html', methods=['POST', 'GET'])
def view_log():
    if request.method=="POST":
        title = request.form['titlelog']
        name = request.form['id']
        date = request.form['timestamp']
        view = [dbHandler.match_log(name, date, title)]
        print(view)
        return render_template('/view_log.html', log=view, cred=session['status'])
    
@app.route('/submitlog.html', methods=['POST', 'GET'])
def submit_log():
    email = session['mail']
    id = dbHandler.get_teams(email)    
    if request.method=="POST":
        return render_template('/submitlog.html', cred=session['status'], teams=id)
    else:
        return render_template('/submitlog.html', cred=session['status'], teams=id)
    
@app.route('/getlog.html', methods=['POST'])
def get_log():
    if request.method=="POST":
        team = request.form['name']
        devlog = dbHandler.get_log(team)
        session['logs'] = devlog
        return home()
    
@app.route('/get_teams.html', methods=['POST'])
def get_teams():
    if request.method=="POST":
        user = dbHandler.get_user(session['mail'])
        title_log = request.form['title']
        subtitle_log = request.form['subtitle']
        log_info = request.form['log']
        date = request.form['timestamp']
        team = session['team']
        dbHandler.insert_log(user, team, date, title_log, subtitle_log, log_info)
        return submit_log()
        
@app.route('/team.html', methods=['POST'])
def team_name():
    if request.method=="POST":
        team = request.form['name']
        session['team'] = team
        return submit_log()

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
    
