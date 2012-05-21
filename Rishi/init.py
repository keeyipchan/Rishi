from Rishi.mind import mind

__author__ = 'Robur'


def start():
    from Rishi import routes


    routes.init()

    import configparser
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    print(type(mind))

    mind.setSources(config['Rishi']['sources'])


    return None