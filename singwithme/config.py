from dataclasses import dataclass
from configparser import ConfigParser

colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

@dataclass
class Config():

    def __init__(self, path):
        parser = ConfigParser()
        parser.read(path)
        self.header_bg = get_color(parser, 'header_bg', 'blue')
        self.header_fg = get_color(parser, 'header_fg', 'black')
        self.body_bg = get_color(parser, 'body_bg', 'default')
        self.body_fg = get_color(parser, 'body_fg', 'white')

def get_color(parser, key, default):
    color = default
    if parser.has_section('colors') and parser.has_option('colors', key):
        color = parser.get('colors', key)
    if color in colors:
        return colors.index(color)
    return -1
