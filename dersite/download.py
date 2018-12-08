#!/usr/bin/env python
# -*- coding: utf-8 -*-


import youtube_dl
from . import utils


def download_info(url, filename):
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
    utils.write_json(filename, info)


def download_channel_info(channel_id, filename):
    if not filename.endswith(".json"):
        filename = filename + ".json"
    download_info(f"https://www.youtube.com/channel/{channel_id}",
                  filename)
    download_info(f"https://www.youtube.com/channel/{channel_id}/playlists",
                  filename.replace(".json",
                                   "_playlists.json"))
