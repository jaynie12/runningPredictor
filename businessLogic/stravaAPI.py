import oauthlib
import requests
import json
import webbrowser
from requests_oauthlib import OAuth2Session 
#explicity state that we cann use HTTP
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import os


client_id = ""  
client_secret = 'HIDEN'
redirect_uri = "http://localhost:8051/oauth2callback"
scope = ["read", "activity:read_all"]


oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

authorization_url, state = oauth.authorization_url(
    "https://www.strava.com/oauth/authorize",
    approval_prompt="force",   # Optional: "auto" or "force"  
)

print(authorization_url)


full_redirect_url = input('Enter redirect URL :: ')

auth_code =oauth.fetch_token(
    "https://www.strava.com/oauth/token",
    authorization_response=authorization_url,
    scope=scope,
    client_secret=client_secret            
)

token = oauth.fetch_token(
   "https://www.strava.com/oauth/token",
    authorization_response= full_redirect_url,  
    code=auth_code,
    client_secret=client_secret  
)

headers = {
    "Authorization: f‘Bearer {access_token}",
    "Content-Type: ‘application/json"  
}

response = requests.get(
    "https://www.strava.com/api/v3/athlete/activities?before=7&after=7&page=1&per_page=10", 
    headers = headers              
)


if __name__=='main':
    print(response.json())