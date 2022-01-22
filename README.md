# singwithme  

For downloading and displaying lyrics for songs that are playing on an MPRIS client.  

## Requirements  
python  
playerctl  
curses

## Usage
Run singwithme_tui.py from the singwithme module's directory. If a song is playing from an MPRIS player and you have an Internet connection, it should display lyrics. Press r to reload the configuration file, h to toggle header visibility, b to toggle body visibility, and q to quit. Lyrics are stored in ~/.cache/singwithme

## Configuration  
Place a file called singwithme.conf in the same directory as the singwithme.py.  
Below is the default configuration:  

    [colors]
    header_bg = blue
    header_fg = black
    body_bg = default
    body_fg = white

    [header]
    format = '!title by !artist'
    visible = true

    [body]
    visible = true

Colors can be any of default, black, red, green, yellow, blue, magenta, cyan, white, or an integer between -1 and 7 inclusive.  
In the header, !title, !artist, and !album get replaced by their actual values when displayed.
