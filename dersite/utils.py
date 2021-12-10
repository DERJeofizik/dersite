# -*- coding: utf-8 -*-

import json
import re

import os
import glob
import shutil

import toml
import datetime


def load_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def slugify(name):
    """Create url friendly version of the texts.

    Mainly converts turkish characters into their url safe versions.
    """
    conversions = {
        " ": "_",
        "ğ": "g",
        "ü": "u",
        "ş": "s",
        "ı": "i",
        "ö": "o",
        "ç": "c",
        ".": "",
        ",": "",
        "/": "_",
        "?": "",
        "'": "",
        "(": "",
        ")": "",
        ":": "",
        "-": "_"
    }
    slug = name.lower()
    for a, b in conversions.items():
        slug = slug.replace(a, b)
    return slug


def slug_entries(entries):
    for entry in entries:
        entry["slug"] = slugify(entry["title"])


def load_youtube_data(filename, channel=False):
    data = load_json(filename)
    if channel:
        slug_entries(data["entries"][0]["entries"])
    else:
        slug_entries(data["entries"])
    return data


def regex_replace(s: str, find: str, replace: str):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)


def copy_files(files, dst_folder):
    """Copy `files` (wildcard) to `dst_folder`"""
    for f in glob.glob(files):
        if os.path.isdir(f):
            folder = f.split("/")[-1]
            new_dst = f"{dst_folder}/{folder}"
            os.makedirs(new_dst, exist_ok=True)
            copy_files(f"{f}/*", new_dst)
        else:
            shutil.copy(f, dst_folder)


def parse_toml(filename_or_str):
    return toml.loads(filename_or_str)


def get_cur_time():
    return datetime.datetime.today()
