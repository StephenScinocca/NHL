import pandas as pd
import argparse as ap
import urllib.request
import json
import os
import pprint as pprint
from urllib.error import URLError, HTTPError, ContentTooShortError

# link = 'http://statsapi.web.nhl.com/api/v1/people/8471214/?hydrate=stats(splits=yearByYear)'
link = 'http://statsapi.web.nhl.com/api/v1/people/8471222/?hydrate=stats(splits=yearByYear)'
## Alex Ovechkin career stats year by year
## has KHL as well as WCA and Olympics, only want NHL
id2 = '8471222'
id = '8471214'
link = 'http://statsapi.web.nhl.com/api/v1/people/{}/?hydrate=stats(splits=yearByYear)'.format(id2)

def download(link, num_retries=2):
    print('Downloading:', link)
    request = urllib.request.Request(link)
    try:
        with urllib.request.urlopen(request) as url:
            html = json.loads(url.read().decode())
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return 0
    return html

data = download(link)

            
player = data['people'][0]['stats'][0]['splits']
seasons = []
headers = []
headers.append('season')
for j in player[14]['stat']:
    headers.append(j)
print(headers)
for i in player:
    season = []
    if i['league']['name'] == 'National Hockey League':
        season.append(i['season'])
        for j in i['stat']:
            season.append(i['stat'][j])
        print(season)
        print()


        
# statistics = pd.DataFrame(season, columns = headers)

# pprint(season)

print(link)