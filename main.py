import spotipy
import json
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

cid = "4621674ac5b94fdeab73a3561b46ab3c"
secret = "abbbe4289b6c430296e26d2ca99ab8f0"
username = "damon.black.dwb"
# space seperated when using multiple scopes
scopes = [
    "user-read-currently-playing",
    "user-modify-playback-state",
    "playlist-modify-public",
    "user-library-read",
    "user-library-modify",
]

scope = " ".join(scopes)

token = util.prompt_for_user_token(
    username,
    scope,
    client_id=cid,
    client_secret=secret,
    redirect_uri="http://127.0.0.1:8000/callback",
)

if token:
    sp = spotipy.Spotify(auth=token)


def get_current_song():
    song_information = sp.currently_playing()["item"]
    song = {
        "artist": song_information["artists"][0]["name"],
        "name": song_information["name"],
        "id": song_information["id"],
        "href": song_information["href"],
    }

    # sp.track(song_information["id"])

    print(json.dumps(song, indent=2))


def get_saved_tracks():
    tracks = sp.current_user_saved_tracks()

    print(json.dumps(tracks["items"][:3], indent=2))


def pause_song():
    sp.pause_playback()


def play_song():
    sp.start_playback()


def like_song():
    song = sp.currently_playing()["item"]["id"]
    sp.current_user_saved_tracks_add([song])


def unlike_song():
    song = sp.currently_playing()["item"]["id"]
    sp.current_user_saved_tracks_delete([song])


def skip_song():
    sp.next_track()


def set_volume(volume):
    sp.volume(int(volume))


def previous_song():
    sp.previous_track()


def toggle_shuffle(status=True):
    sp.shuffle(status)


def toggle_repeat(state="context"):
    sp.repeat(state)


def prompt_for_command(options):
    print("what to do...")
    response = input()

    if response == "shuffle off":
        options[response](False)
    elif response == "repeat song":
        options[response]("track")
    elif response == "repeat off":
        options[response]("off")
    elif "set volume" in response:
        options["set volume"](response.split(" ")[2])
    else:
        if options.get(response) != None:
            options[response]()


def main():
    options = {
        "play": play_song,
        "pause": pause_song,
        "current song": get_current_song,
        # "saved tracks": get_saved_tracks,
        "like": like_song,
        "unlike": unlike_song,
        "shuffle on": toggle_shuffle,
        "shuffle off": toggle_shuffle,
        "repeat": toggle_repeat,
        "repeat song": toggle_repeat,
        "repeat off": toggle_repeat,
        "skip": skip_song,
        "previous": previous_song,
        "set volume": set_volume,
    }

    while True:
        prompt_for_command(options)


main()