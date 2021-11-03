import subprocess as sp
from urllib.parse import unquote
import re
import requests
import os

redirect_pattern = re.compile('.*?uddg=(.*?)&rut=.*')
lyrics_pattern = re.compile('class="Lyrics__Container.*?>(.*?)</div', re.DOTALL)
replacements = {
        '<br>' : '\n',
        '<br/>' : '\n',
        '<br />' : '\n',
        '<.*?>' : '',
        '&#x27;' : '\'',
        '&quot;' : '"',
        '&amp;' : '&'
        }


def fetch_lyrics(name):
    lyrics = cache_lookup(name)
    if not lyrics:
        lyrics = network_lookup(name)
        cache_store(name, lyrics)
    return lyrics


def get_cache_path():
    return os.path.expanduser('~/.cache/singwithme/')


def cache_lookup(name):
    file_name = clean_file_name(name)
    path = get_cache_path()
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.isfile(path + file_name):
        with open(path + file_name, 'r') as file:
            lyrics = file.readlines()
            return lyrics
    return None


def cache_store(name, lyrics):
    file_name = clean_file_name(name)
    path = get_cache_path()
    with open(path + file_name, 'w') as file:
        for line in lyrics:
            file.write(line)


def network_lookup(name):
    search_query = name + ' site:genius.com !'
    url = 'https://duckduckgo.com/'
    headers = {'user-agent': 'lyrics-fetching'}
    params = {'q': search_query}
    response = requests.get(url, params=params, headers=headers)
    redirect_url = unquote(redirect_pattern.match(response.text).group(1))
    response = requests.get(redirect_url)

    lyrics = '\n'.join(lyrics_pattern.findall(response.text))
    lyrics = strip_html(lyrics)
    lyrics = lyrics.splitlines()
    lyrics = [line + '\n' for line in lyrics]
    return lyrics


def clean_file_name(name):
    return re.sub('[^a-zA-Z0-9_\-]*', '', name)


def main():
    format = '{{title}}#@{{artist}}#@{{album}}'
    cmd = 'playerctl -F -p ncspot,spotify,Spotify,%any metadata --format'.split()
    cmd.append(format)
    with sp.Popen(cmd, stdout=sp.PIPE) as process:
        while True:
            title, artist, album = process.stdout.readline().decode('utf-8').split('#@')
            print(str(3))
            print('Title')
            print(title)
            print('Artist')
            print(artist)
            print('Album')
            print(album, end='', flush=True)
            lyrics = fetch_lyrics(title + ' ' + artist)
            print(str(len(lyrics)))
            print(''.join(lyrics), flush=True, end='')


def strip_html(text):
    for key, value in replacements.items():
        text = ''.join(re.sub(key, value, text))
    return text


if __name__ == '__main__':
    main()
