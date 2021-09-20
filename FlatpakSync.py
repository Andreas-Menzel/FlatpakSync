#!/usr/bin/env python3

import argparse
import os.path
import subprocess

### ARGPARSE ###################################################################
parser = argparse.ArgumentParser(description='Save and restore your Flatpak packages!', prog='FlatpakSync')

parser.add_argument('--version', action='version', version='%(prog)s v1.0')
parser.add_argument('-b', '--backup',
    action='store_true',
    help='Create backup.')
parser.add_argument('-i', '--install',
    action='store_true',
    help='Install all Flatpak.')
parser.add_argument('-v', '--verbose',
    action='store_true',
    help='Display info messages.')
parser.add_argument('-f', '--file',
    default="FlatpakSync__installed_apps.txt",
    help='')

args = parser.parse_args()
# end - argparse


def get_installed_apps():
    if args.verbose:
        print("[INFO] Checking file for apps...")

    if not os.path.isfile(args.file):
        if args.verbose:
            print("[INFO] File ", args.file, "does not exist. No apps found.")
        return []

    return_string = ""
    with open(args.file, 'r') as reader:
        return_string = reader.read()

    tmp_apps = return_string.split('\n')[:-1]

    apps = []
    for app in tmp_apps:
        apps.append(app.split('\t'))

    return apps


def create_backup():
    if args.verbose:
        print("[INFO] Creating backup...")

    with open(args.file, 'w') as file:
        subprocess.run(["flatpak", "list", "--columns=origin,application,arch,branch"], stdout=file, text=True).stdout

    if args.verbose:
        print("[INFO] Finished creating backup.")


def install(apps):
    if args.verbose:
        print("[INFO] Installing apps...")

    for app in apps:
        subprocess.run(["flatpak", "install", "--noninteractive", "-y", app[0], app[1] + "/" + app[2] + "/" + app[3]])

    if args.verbose:
        print("[INFO] Finished installing apps.")


if __name__ == '__main__':
    if args.install:
        install(get_installed_apps())

    if args.backup:
        create_backup()
