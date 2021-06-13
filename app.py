from flask import Flask, render_template, request, session, redirect
from oauth import Oauth
import json
from flask_cors import CORS, cross_origin
import json

with open('credentials.json') as f:
    cred = json.load(f)
    SECREAT_KEY = cred['client_secreat']


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = SECREAT_KEY


@app.route("/")
def home():
    user = None
    if 'token' in session:
        user = Oauth.get_user_json(session.get('token'))

    return render_template("index.html", discord_url=Oauth.discord_login_url, auth='token' in session, user=user)


@app.route("/login")
@app.route("/login/")
def login():
    token = Oauth.get_access_token(request.args['code'])
    session['token'] = token

    return redirect('/stats')


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route("/stats")
def stats():

    if 'token' not in session:
        return redirect(Oauth.discord_login_url)

    user = Oauth.get_user_json(session.get('token'))

    Users_Avatar_Link = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}"
    
    try:
        Premium_Type = user['premium_type']
    except:
        Premium_Type = "Failed"

    user_guild_object = Oauth.get_user_current_guild(session.get('token'))

    Total_Server = 0
    your_server = 0
    for i in user_guild_object:
        Total_Server += 1

    for f in user_guild_object:
        if f['owner'] == True:
            your_server += 1

    return render_template("stats.html", avatar=Users_Avatar_Link, pt=Premium_Type, render_guild=user_guild_object, Total_Server=Total_Server, Your_Total_Server=your_server, user=user)


if __name__ == "__main__":
    app.run(debug=True)
