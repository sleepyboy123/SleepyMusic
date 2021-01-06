import os
from mutagen.easyid3 import EasyID3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.error import HTTPError
from mutagen.id3 import ID3NoHeaderError

from secret import *

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

music_dir = "C:/Users/Matthew/Desktop/Stuff/MTZS Music/"

for filename in os.listdir(music_dir):
    if filename.endswith(".mp3"):
        song_name = filename[:-4]
        try:
            audio = EasyID3(music_dir + filename)
            try:
                print(song_name + "'s artist is " + str(audio['artist']))
            except KeyError:
                print('Searching for ' + song_name + ' ...')
                try:
                    searchResults = sp.search(q="track:" + song_name, type="track")
                    try:
                        song_artist = searchResults['tracks']['items'][0]['album']['artists'][0]['name']     
                        audio['artist'] = song_artist
                        audio.save()
                        print('Artist found...')
                    except IndexError:
                        print('Artist not found...')
                except HTTPError as err:
                    print('Track cannot be found...')
        except ID3NoHeaderError:
            print(song_name + ' has a tag error')
