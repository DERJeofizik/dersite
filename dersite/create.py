#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown

import os
import shutil

from . import utils
from .config import Config
from .template import WebsiteCreator


def create(conf: Config, data_filename, base_url=None):
    if base_url:
        conf.base_url = base_url

    for path in conf.output_dir.glob("*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    os.makedirs(conf.output_dir, exist_ok=True)

    c = WebsiteCreator(conf)

    videos_data = utils.load_youtube_data(data_filename, channel=True)

    # Add extra notes
    for entry in videos_data["entries"][0]["entries"]:
        if entry["id"] in conf.extra_notes:
            filename = conf.extra_notes[entry["id"]]
            with open(filename) as f:
                entry["extra_note"] = f.read()

            if filename.endswith(".md"):  # Markdown
                entry["extra_note"] = markdown.markdown(entry["extra_note"])

    playlists_data = utils.load_youtube_data(
        data_filename.replace(".json", "_playlists.json"))

    print("Creating index.html...")
    c.render_to_file("index.html",
                     conf.output_dir / "index.html",
                     entries=videos_data["entries"][0]["entries"],
                     playlists=playlists_data["entries"])

    video_dir = conf.output_dir / "video"
    os.makedirs(video_dir)
    print("Creating video pages...")
    for entry in videos_data["entries"][0]["entries"]:
        c.render_to_file("video.html",
                         video_dir / f"{entry['slug']}.html",
                         entry=entry,
                         playlists=playlists_data["entries"])

    list_dir = conf.output_dir / "liste"
    os.makedirs(list_dir)
    print("Creating playlist pages...")
    for entry in playlists_data["entries"]:
        c.render_to_file("playlist.html",
                         list_dir / f"{entry['slug']}.html",
                         entries=entry["entries"],
                         title=entry["title"],
                         playlists=playlists_data["entries"])

    print("Copying include files...")
    utils.copy_files(str(conf.include_dir / "*"), conf.output_dir)
