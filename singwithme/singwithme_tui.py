import curses
import subprocess as sp
import threading
import singwithme
import sys
from config import Config
from queue import Queue, Empty
from enum import Enum
from textwrap import TextWrapper

text_wrapper = TextWrapper(drop_whitespace=False)

def main(window):
    config = Config('singwithme.conf')
    curses.use_default_colors()
    curses.init_pair(1, config.header_fg, config.header_bg)
    curses.init_pair(2, config.body_fg, config.body_bg)
    curses.halfdelay(2)

    song = singwithme.Song()

    load_songs_t = threading.Thread(target=singwithme.start, args=(song,), 
                                    daemon=True)
    load_songs_t.start()

    while song.playing:
        draw(window, song)
        ch = window.getch()
        if ch == ord('q'):
            song.playing = False
        elif ch == curses.KEY_DOWN:
            song.line_index += 1
        elif ch == curses.KEY_UP:
            song.line_index -= 1
        elif ch == curses.KEY_NPAGE:
            song.line_index += 10
        elif ch == curses.KEY_PPAGE:
            song.line_index -= 10

    draw(window, song)


def draw(window, song):
    curses.curs_set(0)
    window.clear()
    height, width = window.getmaxyx()
    text_wrapper.width = width
    window_row = 0
    for key, value in song.desc.items():
        aligned_desc = align(value, width, ALIGNMENT.CENTER)
        window.addstr(window_row, 0, aligned_desc, curses.color_pair(1))
        window_row += 1
    line_index = song.line_index
    while window_row < height:
        if line_index < 0 or line_index >= len(song.lyrics):
#            window.insstr(window_row, 0, ''.rjust(width), curses.color_pair(2))
            window_row += 1
            line_index += 1
            continue
        wrapped_line = text_wrapper.wrap(song.lyrics[line_index])
        if len(wrapped_line) == 0:
            wrapped_line = ['']
        for line in wrapped_line:
            if window_row >= 0 and window_row < height:
                aligned_line = align(line, width, ALIGNMENT.CENTER)
                window.insstr(window_row, 0, aligned_line, curses.color_pair(2))
                window_row += 1
        line_index += 1
    window.insstr(0, 0, song.status)
    window.refresh()


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

curses.wrapper(main)
