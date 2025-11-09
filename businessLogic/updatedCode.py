import oauthlib
import requests
from requests_oauthlib import OAuth2Session 
#explicity state that we cann use HTTP
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import os


client_id = "182560"  
client_secret = '4eb9fdaa7b1d93f63282327ebb362e3786744901'
redirect_uri = "http://localhost:8051/oauth2callback"
scope = ["read", "activity:read_all"]
apiendpoint= "https://www.strava.com/api/v3/athlete/activities?before=7&after=7&page=1&per_page=10"

import os
import requests
import webbrowser
import json

def initial_authorisation_token():
   
  # send request to server to authorize a user
  # this will prompt the user to sign into strava and grant our application permissions
  request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                        f'&response_type=code&redirect_uri={redirect_uri}' \
                        f'&approval_prompt=force' \
                        f'&scope=profile:read_all,activity:read_all'
  
  # open url in browser
  webbrowser.open(request_url)
  
  # recieve code once user has logged in
  code = input('Insert the code from the url: ')
      
  # Get the access token
  token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                       data={'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'grant_type': 'authorization_code'})
  token = token.json()
 
  # save token for later (function shown below)
  write_token(token)

  return token


def write_token(token):

  with open('strava_token.json', 'w') as file:
    json.dump(token, file)

# read token from file

def read_token():

  try:
      with open('strava_token.json', 'r') as f:
          token = json.load(f)
  except FileNotFoundError:

      # token cannot be found, so cannot be refreshed
      # instead, follow the original authorisation procedure again
      token = initial_authorisation_token()

  return token

import time

# refresh the authorisation token

def refresh_token(token):

    # check if the token has expired
    if token['expires_at'] < time.time():

        # request a new access token using the refresh token
        token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'grant_type': 'refresh_token',
                                   'refresh_token': token['refresh_token']})
        token = token.json()    
        write_token(token)
        
    return token

import pandas as pd

# get & update token first, uses tools described above
token = read_token()
token = refresh_token(token)


# import all user activities

activities = []
page = 1
response = []

while True:
    
    # request new page of activities
    endpoint = f"https://www.strava.com/api/v3/athlete/activities?" \
                  f"access_token={token['access_token']}&" \
                  f"page={page}&" \
                  f"per_page=50"
    
    response = requests.get(endpoint).json()

    # check if page contains activities
    if len(response):

        # retrieve some fields for each activity
        # you can see the full list of fields by looking at the response json
        activities += [{"name": i["name"],
                "distance": i["distance"],
                "type": i["type"],
                "sport_type": i["sport_type"],
                "moving_time": i["moving_time"],
                "elapsed_time": i["elapsed_time"],
                "date": i["start_date"],
                "polyline": i["map"]["summary_polyline"],
                "map_id": i["map"]["id"],
                "start_latlng": i["start_latlng"]} for i in response]
        page += 1  

    else:
      break  

# convert our activities to a D
print(str(activities))