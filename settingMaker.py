from configparser import ConfigParser

# function for the settings creation and checker, called every time the main program is run to make sure a settings file always exists
def configSetup():
    config = ConfigParser()

    config.read('settings.ini')

    #check for settings.ini. If it exists, we good. Otherwise, create with these default values.
    if 'main' in config:
        print("settings.ini already exists!")

    elif 'main' not in config:
        config.add_section('main')
        config.set('main', 'TBA-KEY', '')
        config.set('main', "rounding",'2')
        config.set('main',"stop-time",'35')

        with open('settings.ini', 'w') as f:
            config.write(f)
        print("Settings.ini has been created.")

