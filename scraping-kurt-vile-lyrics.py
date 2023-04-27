
import token
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Genius API access token
CLIENT_ACCESS_TOKEN = token.accessToken


# HTTP authorization header
headers = {
    'User-Agent': 'CompuServe Classic/1.22',
    'Accept': 'application/json',
    'Host': 'api.genius.com',
    'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN
    }


url_base = 'http://api.genius.com/'
request_url = url_base + 'artists/37902/songs' # Kurt Vile songs


results = [0,0,0,0]

# Gather Genius data for every Kurt Vule song and store it in results list
for i in range(1,5):
    response = requests.get(request_url, params = {'per_page' : 50, 'page' : i} , headers=headers)
    results[i-1] = response.json()
    print(results[i-1])

song_names = []
release_year = []
song_paths = []

# for every song, store the song name, release year, and path in its corresponding list
for i in range(0,4):
    for song in results[i]['response']['songs']:
        if song['primary_artist']['api_path'] == '/artists/37902':
            song_names.append(song['title'])
            if song['release_date_components'] is None:
                release_year.append(0)
            else:
                release_year.append(song['release_date_components']['year'])
            song_paths.append(song['path'])
            
# create dataframe with Kurt Vile song data            
kvjamsdict = {'song-name': song_names,'release-year':release_year,'genius-path': song_paths}
kvjams = pd.DataFrame(kvjamsdict)
print(kvjams.head())

# function to scrape song lyrics
def scrape_lyrics(path):
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics = html.find('div', attrs = {'class' :"Lyrics__Container-sc-1ynbvzw-5 Dzxov", 'data-lyrics-container':"true"})
    if lyrics is None:
        return False
    else: 
        for br in lyrics.find_all('br'):
            br.replace_with(' ')
        return lyrics.get_text()


# save song lyrics in a list
songlyrics = []
for path in kvjams['genius-path']:
    songlyrics.append(scrape_lyrics(path))

# add song lyrics column to dataframe
kvjams.insert(1,'lyrics', songlyrics)
print(kvjams.head())

# save dataframe as a CSV file
kvjams.to_csv("kurt-vile-song-lyrics.csv")


