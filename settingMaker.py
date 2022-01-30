from configparser import ConfigParser

def configSetup():
    config = ConfigParser()

    config.read('settings.ini')

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

