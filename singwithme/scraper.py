import re
import requests
from urllib.parse import unquote

replacements = {
        '<br>' : '\n',
        '<br/>' : '\n',
        '<br />' : '\n',
        '<.*?>' : '',
        '&#x27;' : '\'',
        '&quot;' : '"',
        '&amp;' : '&'
        }

redirect_pattern = re.compile('.*?uddg=(.*?)&rut=.*')

class Scraper:
    def scrape(self, song_info):
        search_query = song_info + ' site:' + self.site + ' !'
        url = 'https://duckduckgo.com/'
        headers = {'user-agent': 'lyrics-fetching'}
        params = {'q': search_query}
        response = requests.get(url, params=params, headers=headers)
        redirect_url = unquote(redirect_pattern.match(response.text).group(1))
        response = requests.get(redirect_url)

        lyrics = '\n'.join(self.pattern.findall(response.text))
        lyrics = strip_html(lyrics)
        lyrics = lyrics.splitlines()
        lyrics = [line + '\n' for line in lyrics]
        return lyrics


    def __init__(self, site, regex):
        self.site = site
        self.pattern = re.compile(regex, re.DOTALL)
    

def strip_html(text):
    for key, value in replacements.items():
        text = ''.join(re.sub(key, value, text))
    return text
