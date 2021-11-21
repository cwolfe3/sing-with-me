# singwithme  

A Linux TUI for downloading and displaying lyrics for the currently playing song.  

## Requirements  
Python  
Playerctl  

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
    format = '!title\n!artist\n!album'
    visible = true

    [body]
    visible = true

Colors can be any of default, black, red, green, yellow, blue, magenta, cyan, white, or an integer between -1 and 7 inclusive.  
The header format is a \n-delimited string. !title, !artist, and !album are replaced by their actual values when displayed.
