import requests
import time
import pandas

# Setuping the scraper
base_url = "https://api.jikan.moe/v4/anime?page="
page = 1
all_animes = []
total_animes = 0 
running = True 

# loop
while running:

    # Getting all
    response = requests.get(base_url+str(page))
    data = response.json()
    
    # Each anime is in there own dictionary 
    all_animes.extend(data['data'])
    print("On page:" + str(page) + "\nCurrently collected: " + str(len(all_animes)) + " animes")
    page += 1

     # No more pages, thus stopping the loop
    if not data['pagination']['has_next_page']:
        running = False

    time.sleep(1)


# Time to extract useful information and format it into a csv file
all_animes_rows = []

for anime in all_animes:
    row = {
        'mal_id': anime['mal_id'], 
        'title': anime['title'], 
        'title_en': anime['title_english'], 
        'title_synonyms': anime['title_synonyms'], 
        'type': anime['type'], 
        'source': anime['source'], 
        'episodes': anime['episodes'], 
        'status': anime['status'], 
        'airing': anime['airing'], 
        'duration': anime['duration'], 
        'rating': anime['rating'], 
        'score': anime['score'], 
        'scored_by': anime['scored_by'], 
        'rank': anime['rank'], 
        'popularity': anime['popularity'], 
        'members': anime['members'], 
        'favorites': anime['favorites'], 
        'synopsis': anime['synopsis'], 
        'season': anime['season'], 
        'year': anime['year'], 
        'year_2':anime['aired']['prop']['from']['year'], # Hoping to get the year and month correctly from using this (Since there are some nulls)
        'month': anime['aired']['prop']['from']['month'],
        'licensors': [licensor['name'] for licensor in anime['licensors']], 
        'producers': [producer['name'] for producer in anime['producers']], 
        'studios': [studio['name'] for studio in anime['studios']], 
        'genres':[ genre['name'] for  genre in anime['genres']], 
        'explict_genres': [ genre['name'] for  genre in anime['explicit_genres']], 
        'themes': [theme['name'] for theme in anime['themes']] 
    }

    all_animes_rows.append(row)

all_anime_df = pandas.DataFrame(all_animes_rows)
all_anime_df.to_csv('anime_data_fixed.csv', sep=',', index=False, encoding='utf-8')
