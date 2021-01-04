import os
import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.error import HTTPError

from secret import *

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

music_dir = "C:/Users/Matthew/Desktop/Stuff/MTZS Music/"

for filename in os.listdir(music_dir):
    if filename.endswith(".mp3"):
        audiofile = eyed3.load(music_dir + filename)
        if audiofile.tag != None and audiofile.tag.artist == None:
            song_name = filename[:-4]
            print('Searching for ' + song_name + ' ...')
            try:
                searchResults = sp.search(q="track:" + song_name, type="track")
                try:
                    song_artist = searchResults['tracks']['items'][0]['album']['artists'][0]['name']     
                    audiofile.tag.artist = song_artist
                    print('Artist found...')
                except IndexError:
                    print(song_artist)
            except HTTPError as err:
                print('Track cannot be found...')
            audiofile.tag.save(version=(1,None,None))
            audiofile.tag.save()
