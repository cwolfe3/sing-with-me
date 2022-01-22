import subprocess as sp
import os
import re
from scraper import Scraper

scrapers = [
        Scraper('genius.com', 'class="Lyrics__Container.*?>(.*?)</div'),
        Scraper('azlyrics.com', 'class="lyricsh">.*?<div>.*?>(.*?)</div'),
        ]

def fetch_lyrics(name):
    lyrics = cache_lookup(name)
    if not lyrics:
        lyrics = network_lookup(name)
        if lyrics:
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
    for scraper in scrapers:
        lyrics = scraper.scrape(name)
        if lyrics:
            return lyrics
    return None


def clean_file_name(name):
    return re.sub('[^a-zA-Z0-9_\-]*', '', name)


class Song:
    desc = {}
    lyrics = []
    line_index = 0
    playing = True
    status = ''


def start(song):
    format = '{{title}}#@{{artist}}#@{{album}}'
    cmd = 'playerctl -F -p ncspot,spotify,Spotify,%any metadata --format'.split()
    cmd.append(format)
    song.playing = True
    with sp.Popen(cmd, stdout=sp.PIPE) as process:
        while True:
            title, artist, album = process.stdout.readline().decode('utf-8').split('#@')
            song.desc['title'] = title
            song.desc['artist'] = artist
            song.desc['album'] = album.strip('\n')
            song.lyrics = ['Loading...']
            lyrics = fetch_lyrics(title + ' ' + artist + ' ' + album)
            if not lyrics:
                lyrics = ['Either no lyrics were found, or there\'s a network error.']
            song.lyrics = lyrics


