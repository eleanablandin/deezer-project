from flask import Flask, redirect, request
from flask_oauthlib.client import OAuth
import requests
import pandas as pd 


app = Flask(__name__)

flask_key = open('flask_key.txt', 'r').read().splitlines()
app.secret_key = flask_key[0]

##deezer api keys
deezer_keys = open('deezer.txt', 'r').read().splitlines()
id_key = deezer_keys[0]
secret_key = deezer_keys[1]

## Deezer credential settings 
deezer = OAuth(app).remote_app(
    'deezer',
    consumer_key=id_key,
    consumer_secret=secret_key,
    base_url='https://api.deezer.com/',
    request_token_params={'scope': 'basic_access,email'},
    request_token_url=None,
    access_token_url='https://connect.deezer.com/oauth/access_token.php',
    authorize_url='https://connect.deezer.com/oauth/auth.php'
)

## Login 
@app.route('/login')
def login():
    callback_url = request.url_root + 'callback'
    return deezer.authorize(callback=callback_url or None)

## function to get token 
@app.route('/callback')
def callback():
    resp = deezer.authorized_response()

    if resp is None:
        return 'Acceso denegado: Razón: {} error: {}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    access_token = resp['access_token']

    return 'Token de acceso obtenido: {}'.format(access_token)


if __name__ == '__main__':
    app.run(debug=True)
