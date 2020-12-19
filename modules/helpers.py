import sys
from os import path, makedirs

# from xml.dom.minidom import parseString, getDOMImplementation
# import xml.etree.ElementTree as ET

import re

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


def fake_table_to_list(html: str):
    #
    test_header = re.search(r'<div class="header-row">([^"]*)</div><div class="data-row">', html)
    headers = []
    if test_header:
        headers = test_header.groups()[0].replace('<div>', '').split("</div>")[:-1]  # closing /div
    test_content = re.search(r'<div class="data-row">(.*)</div></div></div>', html)
    try:
        error_content = re.search(r'<p class="error">(.*)</p>', html).groups()[0]
    except Exception:
        error_content = None
    values = []
    if test_content:
        content = test_content.groups()[0].replace('<div>', '')\
            .replace('<div class="extra-wrap">', '') \
            .replace('<div class="data-row">', '') \
            .split("</div>")
        while len(content) >= len(headers):
            part = content[0:len(headers)]
            content = content[len(headers)+1:]
            values.append(dict(zip(headers, part)))
    if error_content:
        values.append({"error": error_content})
    return values


def fake_table_frozen_to_dict(html: str):
    """Neither clean nor future proof, but that's the way client sends back the data"""
    try:
        height = re.search(r'<div>height</div><div>([^<]*)</div>', html).groups()[0]
    except Exception:
        height = 0
    try:
        hash = re.search(r'<div>hash</div><div[^>]*>([^<]*)</div>', html).groups()[0]
    except Exception:
        hash = b''
    try:
        timestamp = re.search(r'<div>verification timestamp \(ms\)</div><div>([^<]*)</div>', html).groups()[0]
    except Exception:
        timestamp = 0
    try:
        distance = re.search(r'<div>distance from open edge</div><div>([^<]*)</div>', html).groups()[0]
    except Exception:
        distance = 0
    values = {"height": int(height), "hash": hash.replace('-', ''),
              "timestamp": timestamp, "distance": distance}
    return values
