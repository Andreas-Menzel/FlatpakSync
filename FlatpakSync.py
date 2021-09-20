#!/usr/bin/env python3

import subprocess
import os.path


def get_installed_apps():
    if not os.path.isfile('FlatpakSync__installed_apps.txt'):
        return []

    return_string = ""
    with open('FlatpakSync__installed_apps.txt', 'r') as reader:
        return_string = reader.read()

    tmp_apps = return_string.split('\n')[:-1]

    apps = []
    for app in tmp_apps:
        apps.append(app.split('\t'))

    return apps

def write_to_file():
    with open('FlatpakSync__installed_apps.txt', 'w') as file:
        subprocess.run(["flatpak", "list", "--columns=origin,application,arch,branch"], stdout=file, text=True).stdout
    pass


def install(apps):
    for app in apps:
        subprocess.run(["flatpak", "install", "--noninteractive", "-y", app[0], app[1] + "/" + app[2] + "/" + app[3]])


if __name__ == '__main__':
    write_to_file()
    install(get_installed_apps())
    pass
