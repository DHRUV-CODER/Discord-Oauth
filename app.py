from flask import Flask, render_template, request, session, redirect
from oauth import Oauth
import json
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = "" #secreat-key


@app.route("/")
def home():
    if 'token' in session:
        auth = True
    else:
        auth = False

    return render_template("index.html", discord_url=Oauth.discord_login_url, auth=auth)


@app.route("/login")
@app.route("/login/")
def login():
    token = Oauth.get_access_token(request.args.get("code"))
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

    Avatar = user['avatar']
    Id = user['id']
    Username = user['username']
    Discriminator = user['discriminator']
    Verified = user['verified']
    Email = user['email']
    Users_Avatar_Link = f"https://cdn.discordapp.com/avatars/{Id}/{Avatar}"
    Locale = user['locale']
    Flags = user['flags']
    try:
        Premium_Type = user['premium_type']
    except:
        Premium_Type = "Failed"
    Two_FA_Enabled = user['mfa_enabled']
    
    user_guild_object = Oauth.get_user_current_guild(session.get('token'))
    in_json = json.dumps(user_guild_object)
    
    Total_Server = 0 
    your_server = 0
    for i in user_guild_object:
        Total_Server += 1
        
    
    for f in user_guild_object:
       if f['owner'] == True:
        your_server += 1
       
        
    return render_template("stats.html", avatar=Users_Avatar_Link, id=Id, username=Username, email=Email, discriminator=Discriminator,locale=Locale,flags=Flags,pt=Premium_Type,Two_FA_Enabled=Two_FA_Enabled,render_guild=user_guild_object,Total_Server=Total_Server,Your_Total_Server=your_server)

    
if __name__ == "__main__":
    app.run(debug=True)
