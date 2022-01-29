from configparser import ConfigParser


config = ConfigParser()

config.read('settings.ini')
config.add_section('main')
config.set('main', 'TBA-KEY', '')
config.set('main', "rounding",'2')
config.set('main',"stop-time",'35')

with open('settings.ini', 'w') as f:
    config.write(f)
