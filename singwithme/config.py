from configparser import SafeConfigParser

colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
defaults = {
        'colors': {
            'header_bg': 'blue',
            'header_fg': 'black',
            'body_bg': 'default',
            'body_fg': 'white',
            },
        'header': {
            'format': '!title\n!artist\n!album',
            'visible': True,
            },
        'body': {
            'visible': True,
            }
    }

def load_config(path=''):
    config = SafeConfigParser(strict=False)
    config.read_dict(defaults)
    config.read(path)

    for section in config.sections():
        if section not in defaults.keys():
            continue
        for key, value in config.items(section):
            if key not in defaults[section].keys():
                raise Exception('Unsupported config key: ' + key)

    for key, color in config['colors'].items():
        if color in colors:
            config.set('colors', key, str(colors.index(color)))
        elif color == 'default':
            config.set('colors', key, str(-1))
        elif int(color) not in range(-1, 8):
            raise Exception('Invalid color: ' + color, str(key))
    return config
