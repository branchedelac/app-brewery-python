import json

from spotify_communicator import SpotifyCommunicator
from billboard_scraper import BillboardScraper

spotify = SpotifyCommunicator()
billboard = BillboardScraper()
test_mode = False

# Run
if test_mode:
    # Avoid web scraping unless necessary
    date = "Test Date"
    with open("test_data.json") as f:
        songs = json.load(f)["songs"]
else:
    date = input("Which date do you want to create a playlist for? (YYYY-MM-DD) ")

    print("Getting songs from the Billboard Hot 100 page...")
    soup = billboard.scrape_billboard_hot_100(date)
    songs = billboard.parse_soup(soup)

# Get Spotify URIs for the Hot 100 songs
print("Searching for songs in Spotify...")
song_uris = spotify.find_song_by_keyword(songs)

# Create a new playlist (or update an existing one)
print("Creating a Spotify playlist with the Billboard 100 songs...")

playlist_id, playlist_url = spotify.create_new_playlist(date)

# Add songs to playlist
spotify.add_songs_to_playlist(playlist_id, song_uris)

print(f"Check out your new {date} Billboard Hot 100 playlist over at {playlist_url}!")
