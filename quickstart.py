import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser
import os 
import random

os.environ['SPOTIPY_CLIENT_ID'] = 'cf12cd519a3f4b50bd4d46036a198cf4'
os.environ['SPOTIPY_CLIENT_SECRET'] = '84550a3481294d4a98e63d83e8283a2a'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:3000/'

scope = "user-library-read"
scope2 = "app-remote-control"
scope3 = "streaming"
config = configparser.ConfigParser()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=[scope, scope2, scope3]))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])


playlists = sp.user_playlists('ahaan_chaudhuri')
link = playlists['items'][1]['href']
link2 = playlists['items'][2]['href']
print(playlists['items'][1]['name'], playlists['items'][2]['name'])
locallist = []

#adds all the users playlists to a local list so we don't have to keep refreshing
while playlists:
    for playlist in playlists['items']:
        locallist.append(playlist)
        #print(playlist['name'])
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

def shuffle(lists, size):
    combinedlist = []
    newlist = []
    #add each list in lists to the combined list 
    for curr in lists:
        items = sp.playlist_items(curr['id'])['items']

        for i in items:
            combinedlist.append(i['track'])

    for i in range(size):
        newlist.append(random.choice(combinedlist))

    return newlist

 
shuffled = shuffle([locallist[2], locallist[4]], 10)
for i in shuffled:
    print(i['name'])
    uri = i['uri']
    print(sp.audio_features(tracks=[uri]))
    sp.add_to_queue(uri)
