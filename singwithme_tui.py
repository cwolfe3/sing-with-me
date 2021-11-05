import curses
import subprocess as sp
import threading
from queue import Queue, Empty
from enum import Enum
from textwrap import TextWrapper

text_wrapper = TextWrapper(drop_whitespace=False)

def main(window):
    curses.init_pair(1, 0, 4)
    curses.curs_set(0)

    song = Song()
    que = Queue()

    load_songs_t = threading.Thread(target=load_songs, 
                                    args=(window, song, que))
    load_songs_t.start()

    cmd = 'python singwithme.py'.split()
    proc = sp.Popen(cmd, stdout=sp.PIPE)
    read_songs_t = threading.Thread(target=read_songs, args=(proc.stdout, que))
    read_songs_t.daemon = True
    read_songs_t.start()

    while song.playing:
        draw(window, song)
        try:
            ch = window.getch()
        except:
            song.playing = False
            break 
        if ch == ord('q'):
            song.playing = False
        elif ch == curses.KEY_DOWN:
            song.row += 1
        elif ch == curses.KEY_UP:
            song.row -= 1
        elif ch == curses.KEY_NPAGE:
            song.row += 10
        elif ch == curses.KEY_PPAGE:
            song.row -= 10

    load_songs_t.join()


def draw(window, song):
    height, width = window.getmaxyx()
    text_wrapper.width = width
    window.clear()
    i = 0
    for key, value in song.desc.items():
        aligned_desc = align(value, width, ALIGNMENT.CENTER)
        window.addstr(i, 0, aligned_desc, curses.color_pair(1))
        i += 1
    line_index = song.row
    display_line_index = 4
    while display_line_index < height:
        if line_index < 0 or line_index >= len(song.lyrics):
            display_line_index += 1
            line_index += 1
            continue
        wrapped_line = text_wrapper.wrap(song.lyrics[line_index])
        for line in wrapped_line:
            if display_line_index >= 0 and display_line_index < height - 1: #?
                aligned_line = align(line, width, ALIGNMENT.CENTER)
                window.addstr(display_line_index, 0, aligned_line)
                display_line_index += 1
        if len(wrapped_line) == 0:
            display_line_index += 1
        line_index += 1
    window.addstr(0, 0, song.status)
    window.refresh()


def read_songs(out, que):
    while True:
        que.put(out.readline().decode('utf-8'))


def load_songs(window, song, que):
    #curses.halfdelay(1)
    while song.playing:
        try:
            num_desc = int(que.get(block=True, timeout=0.1))
            song.desc = {}
            for i in range(num_desc):
                key = que.get().strip('\n')
                value = que.get().strip('\n')
                song.desc[key] = value

            song.lyrics = ['Loading...']
            draw(window, song) # In case we need to wait for lyrics
            song.lyrics = []
            num_lines = int(que.get())
            for i in range(num_lines):
                line = que.get().strip('\n')
                song.lyrics.append(line)
            song.row = 0
            draw(window, song)
        except Empty:
            if not song.playing:
                break


class ALIGNMENT(Enum):
    LEFT = -1
    CENTER = 0
    RIGHT = 1


def align(text, width, alignment):
    if len(text) >= width:
        text = text[:width]
    elif alignment == ALIGNMENT.LEFT:
        text = text.ljust(width)
    elif alignment == ALIGNMENT.RIGHT:
        text = text.rjust(width)
    elif alignment == ALIGNMENT.CENTER:
        extra = width - len(text)
        left_pad = extra // 2
        right_pad = extra - left_pad
        text = (' ' * left_pad) + text + (' ' * right_pad)
    return text


class Song:
    desc = {}
    lyrics = []
    row = 0
    playing = True
    status = ''


curses.wrapper(main)
