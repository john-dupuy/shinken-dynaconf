from dynaconf import settings

with open(settings.find_file("settings.cfg")) as settings_file:
    print("settings from cfg file\n", settings_file.read())
