import json
import time

from spotify_communicator import SpotifyCommunicator
from billboard_scraper import BillboardScraper

spotify = SpotifyCommunicator()
billboard = BillboardScraper()
test_mode = False


def get_first_title_match(tracks, song):
    for idx, track in enumerate(tracks):
        if song["title"].lower() in track["name"].lower() or track["name"].lower() in song["title"].lower():
            return track["uri"]
        else:
            get_first_title_match(tracks[idx + 1:], song)

# Run
date = input("Which date do you want to create a platlist for? (YYYY-MM-DD) ")

if test_mode:
    date = "1989-05-21"
    with open("billboard_100.json") as f:
        songs = json.load(f)["songs"]
else:
    print("Getting songs from the Billboard page...")
    soup = billboard.scrape_billboard_hot_100(date)
    songs = billboard.parse_soup(soup)

# Get Spotify URIs for songs
print("Searching for songs in Spotify...")
song_uris = []
for song in songs:
    search_term = f"{song['artist']} {song['title']}"
    tracks = spotify.search_track_by_keyword(search_term)

    if match := get_first_title_match(tracks, song):
        song_uris.append(match)
    else:
        print(f"No matching Spotify track found for: {song['artist']} - {song['title']}")

print("Creating a Spotify playlist with the Billboard 100 songs...")
# Create a new playlist (or update an existing one)
playlist_id = spotify.create_new_playlist(date)

# Add songs to playlist
time.sleep(10)
spotify.add_songs_to_play_list(playlist_id, song_uris)
