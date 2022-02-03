from configparser import ConfigParser
from os.path import exists as file_exists

# function for the settings creation and checker, called every time the main program is run to make sure a settings file always exists
def configSetup():
    config = ConfigParser()

    config.read('settings.ini')

    #check for settings.ini. If it exists, we good. Otherwise, create with these default values.
    if file_exists('settings.ini'):
        print("settings.ini already exists!")

    else:
        config.add_section('main')
        #Need to make a way to ask the user for key on first time startup
        config.set('main', 'TBA-KEY', '')
        config.set('main', "rounding",'2')
        config.set('main',"stop-time",'35')

        with open('settings.ini', 'w') as f:
            config.write(f)
        print("Settings.ini has been created.")

