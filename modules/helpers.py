import sys
from os import path, makedirs

# Where the wallets and other potential private info are to be stored.
# It's a dir under the user's own home directory.
PRIVATE_SUB_DIR = 'nyzo-private'


def get_private_dir():
    """Returns the user's Nyzo private dir"""
    home = path.expanduser('~')
    location = path.join(home, PRIVATE_SUB_DIR)
    if not path.isdir(location):
        makedirs(location, exist_ok=True)
    return location


def base_path():
    """Returns the full path to the current dir, whether the app is frozen or not."""
    if getattr(sys, 'frozen', False):
        # running in a bundle
        locale_path = path.dirname(sys.executable)
    else:
        # running live
        locale_path = path.abspath(path.dirname(sys.argv[0]))
    print("Local path", locale_path)
    return locale_path


def extract_status_lines(status: list, key:str) -> list:
    """Extract the required value from its key
    for extended values, return a list. Ex for frozen edge: ['1695783', '(ajmo2-1.)']
    """
    result = tuple()
    for line in status:
        if line.startswith(key):
            _, value = line.split(':')
            value = value.strip()
            return value.split(' ')
