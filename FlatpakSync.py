#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# FlatpakSync
#
# Easily save and restore all installed Flatpak packages.
#
# https://github.com/Andreas-Menzel/FlatpakSync
#-------------------------------------------------------------------------------
# @author: Andreas Menzel
# @license: MIT License
# @copyright: Copyright (c) 2021 Andreas Menzel
#-------------------------------------------------------------------------------

import argparse
import os.path
from signal import signal, SIGINT
import subprocess

### ARGPARSE ###################################################################
parser = argparse.ArgumentParser(description='Save and restore your Flatpak apps!', prog='FlatpakSync')

parser.add_argument('--version', action='version', version='%(prog)s v1.1')
parser.add_argument('-b', '--backup',
    action='store_true',
    help='Create a list of all installed Flatpak apps.')
parser.add_argument('-i', '--install',
    action='store_true',
    help='Install all Flatpak apps listed in a file.')
parser.add_argument('-f', '--file',
    default="FlatpakSync__installed_apps.txt",
    help='Specify the filename where the Flatpak apps list is stored.')

args = parser.parse_args()
# end - argparse


# get_installed_apps
#
# Reads the list of installed packages from a file and returns it.
#
# @return   [string]    The list of installed packages listed in the file.
def get_installed_apps():
    if not os.path.isfile(args.file):
        print('File', '"' + args.file + '"', 'does not exist.')
        return []

    return_string = ""
    with open(args.file, 'r') as reader:
        return_string = reader.read()

    tmp_apps = return_string.split('\n')[:-1]

    apps = []
    for app in tmp_apps:
        apps.append(app.split('\t'))

    return apps


# create_backup
#
# Get the installed packages and save them in a file.
#
# @return   None
def create_backup():
    with open(args.file, 'w') as file:
        subprocess.run(["flatpak", "list", "--columns=origin,application,arch,branch"], stdout=file, text=True).stdout


# install
#
# Install a given list of packages.
#
# @param    [string]    apps    List of apps to install.
#
# @return   None
def install(apps):
    for app in apps:
        subprocess.run(["flatpak", "install", "--noninteractive", "-y", app[0], app[1] + "/" + app[2] + "/" + app[3]])


# end
#
# Ends the script.
#
# @param    int         sig     Signal.
# @param    FrameType   frame   Frame.
#
# @return   None
def end(sig, frame):
    print("Goodbye!")
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, end)

    if args.install:
        install(get_installed_apps())

    if args.backup:
        create_backup()
