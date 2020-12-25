import spotipy 
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

cid = '4621674ac5b94fdeab73a3561b46ab3c'
secret = 'abbbe4289b6c430296e26d2ca99ab8f0'
username = 'damon.black.dwb'
#space seperated when using multiple scopes
scope = 'user-read-currently-playing user-modify-playback-state' 

token = util.prompt_for_user_token(username, 
                                   scope, 
                                   client_id=cid, 
                                   client_secret=secret, 
                                   redirect_uri="http://127.0.0.1:8000/callback")

if token:
  sp = spotipy.Spotify(auth=token)

def get_current_song():
  song_information = sp.currently_playing()["item"]

  print(song_information)

def pause_song():
  sp.pause_playback()


def main():
  while True:
    get_current_song()
  pass

get_current_song()
pause_song()