import requests
import json

with open('credentials.json') as f:
    cred = json.load(f)
    CLIENT_SECREAT = cred['client_secreat']


class Oauth:
    client_id = "792426758829768744"
    client_secret = CLIENT_SECREAT
    redirect_uri = "https://dsc-dashboard.herokuapp.com/login"
    scope = "identify%20email%20guilds"
    discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20email%20guilds"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"

    @staticmethod
    def get_access_token(code):
        data = {
            "client_id": Oauth.client_id,
            "client_secret": Oauth.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Oauth.redirect_uri,
            "scope": Oauth.scope
        }

        access_token = requests.post(
            url=Oauth.discord_token_url, data=data).json()
        return access_token.get("access_token")

    @staticmethod
    def get_user_json(access_token):
        url = f"{Oauth.discord_api_url}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_object = requests.get(url=url, headers=headers).json()
        return user_object

    @staticmethod
    def get_user_current_guild(access_token):
        user_guild_object = requests.get(
            url=f'{Oauth.discord_api_url}/users/@me/guilds',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_guild_object
