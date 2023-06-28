import random
import string
import re
import time

from dotenv import load_dotenv
import requests
import os
import base64


class SpotifyCommunicator:
    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.token = os.getenv("SPOTIFY_TOKEN")
        try:
            self.bearer_header = {"Authorization": f"Bearer  {self.token}"}
            self.user_id = self.get_authorized_user()["id"]
        except requests.exceptions.HTTPError:
            self.auth_code = self.get_authorization_code()
            self.token = self.get_token()
            self.bearer_header = {"Authorization": f"Bearer  {self.token}"}
            self.user_id = self.get_authorized_user()["id"]

    def get_authorization_code(self):
        url = 'https://accounts.spotify.com/authorize'
        state = ''.join([random.choice(string.ascii_uppercase +
                                       string.ascii_lowercase +
                                       string.digits)
                         for n in range(16)])
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"response_type": "code",
                  "client_id": self.client_id,
                  "client_secret": self.client_secret,
                  "scope": "playlist-modify-private playlist-modify-public",
                  "redirect_uri": self.redirect_uri,
                  "state": state}
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()

        os.system(f"start \"\" {response.url}")
        redirected = input("Please enter the URL of the page that opened: ")
        auth_code = re.search(r'code=(.*?)&state=', redirected).group(1)
        return auth_code

    def get_token(self):
        auth_bytes = f"{self.client_id}:{self.client_secret}".encode("ascii")
        auth_base64 = base64.b64encode(auth_bytes).decode("ascii")
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Authorization": f"Basic {auth_base64}"
                   }

        params = {
            "grant_type": "authorization_code",
            "code": self.auth_code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(url=url, headers=headers, params=params)
        response.raise_for_status()
        token = response.json()["access_token"]

        self.replace_token_in_dotenv(token)
        return token

    def get_authorized_user(self):
        response = requests.get("https://api.spotify.com/v1/me", headers=self.bearer_header)
        response.raise_for_status()
        return response.json()

    def replace_token_in_dotenv(self, token):
        with open(".env", "r") as f:
            lines = f.readlines()
        values = [v.replace('\n', '') for v in lines if "SPOTIFY_TOKEN" not in v]
        values.append(f"SPOTIFY_TOKEN={token}")
        with open(".env", "w") as f:
            print(*values, file=f, sep="\n")

    def find_song_by_keyword(self, songs: list) -> list:
        url = "https://api.spotify.com/v1/search"
        song_uris = []
        for song in songs:
            search_term = f"{song['artist']} {song['title']}"
            params = {"q": search_term,
                      "limit": 20,
                      "type": "track",
                      "market": "SE"}
            response = requests.get(url=url, headers=self.bearer_header, params=params)
            response.raise_for_status()

            tracks = response.json()["tracks"]["items"]
            first_title_match = self.get_first_title_match(tracks, song)
            if first_title_match:
                song_uris.append(first_title_match)
            else:
                print(f"No matching Spotify track found for: {song['artist']} - {song['title']}")
        return song_uris

    def get_first_title_match(self, tracks, song):
        for idx, track in enumerate(tracks):
            if song["title"].lower() in track["name"].lower() or track["name"].lower() in song["title"].lower():
                return track["uri"]
            else:

                self.get_first_title_match(tracks[idx + 1:], song)

    def get_user_playlists(self):
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.get(url=url, headers=self.bearer_header)
        playlists = response.json()["items"]
        return playlists

    def create_new_playlist(self, date):
        playlist_name = f"{date} Billboard 100"
        existing_playlists = self.get_user_playlists()
        duplicate_playlists = [p["id"] for p in existing_playlists if p["name"] == playlist_name]

        if duplicate_playlists:
            use_existing = input("Do you want to update the existing playlist with this name, or create a new one? (update/create) ")
            if use_existing == "update":
                return duplicate_playlists[0]
            else:
                playlist_name = f"{playlist_name} - v. {str(len(duplicate_playlists) + 1)}"

        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        headers = {**self.bearer_header, **{"Content-Type": "application/json"}}
        payload = {
            "name": playlist_name,
            "description": "Playlist generated from Billboard Hot 100 list using web scraping and Spotify APIs.",
            "public": True,
        }
        response = requests.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        playlist_info = response.json()
        print(
            f"New playlist created for {self.user_id}: {playlist_info['name']}"
        )
        playlist_id = playlist_info["id"]
        playlist_url = playlist_info['external_urls']['spotify']
        return playlist_id, playlist_url

    def add_songs_to_playlist(self, playlist_id, song_uris):
        time.sleep(10)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {**self.bearer_header, **{"Content-Type": "application/json"}}
        payload = {
            "uris": song_uris,
        }
        response = requests.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"\nSuccessfully added {len(song_uris)} songs to playlist!")

    @staticmethod
    def get_artist_by_id(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        response = requests.get(url=url, headers=self.bearer_header)
        response.raise_for_status()