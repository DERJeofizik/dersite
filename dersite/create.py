#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown

import os
import shutil

from . import utils
from .config import Config
from .template import WebsiteCreator

def create_pages(conf: Config):
    # Preparing pages
    pages = {}
    for page in conf.pages_dir.glob("*"):
        name = page.stem
        info = {"title": name, "subtitle": "",
                "slug": utils.slugify(name.lower())}
        if page.suffix == ".md":
            info["filetype"] = "markdown"
        elif page.suffix == ".html":
            info["filetype"] = "html"
        else:
            # unsupported filetype
            continue

        with open(page) as f:
            page_content = f.read()

        info["content"] = page_content

        if page_content.startswith("+++\n"):
            if page_content.count("+++\n") < 2:
                raise Exception("Page markdown toml front matter line found (+++) but ending couldn't be found.")
            data = page_content.split("+++\n")
            front_matter = utils.parse_toml(data[1])
            info.update(front_matter)
            # Maybe content has +++ as well, we can reintroduce them here.
            info["content"] = "+++\n".join(data[2:])

        pages[name] = info


    return pages


def create(conf: Config, data_filename, base_url=None):
    if base_url:
        conf.base_url = base_url

    for path in conf.output_dir.glob("*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    os.makedirs(conf.output_dir, exist_ok=True)


    pages = create_pages(conf)

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

    # common data to pass to the templates
    common_data = {
        "playlists": playlists_data["entries"],
        "pages": pages,
        "video_url": "video",
        "page_url": "sayfa",
        "list_url": "liste",
        "published_date": utils.get_cur_time()
    }
    c = WebsiteCreator(conf, common_data)

    print("Creating index.html...")
    c.render_to_file("index.html",
                     conf.output_dir / "index.html",
                     entries=videos_data["entries"][0]["entries"])

    video_dir = conf.output_dir / common_data["video_url"]
    os.makedirs(video_dir)
    print("Creating video pages...")
    for entry in videos_data["entries"][0]["entries"]:
        c.render_to_file("video.html",
                         video_dir / f"{entry['slug']}.html",
                         entry=entry)

    list_dir = conf.output_dir / common_data["list_url"]
    os.makedirs(list_dir)
    print("Creating playlist pages...")
    for entry in playlists_data["entries"]:
        c.render_to_file("playlist.html",
                         list_dir / f"{entry['slug']}.html",
                         entries=entry["entries"],
                         title=entry["title"])

    print("Copying include files...")
    utils.copy_files(str(conf.include_dir / "*"), conf.output_dir)

    print("Creating Pages...")
    page_dir = conf.output_dir / common_data["page_url"]
    os.makedirs(page_dir)
    for page, info in pages.items():
        url = page_dir / (info["slug"]+".html")
        if info["filetype"] == "markdown":
            info["content"] = markdown.markdown(info["content"])
            c.render_to_file("page.html", url,
                             **info)
        elif info["filetype"] == "html":
            c.render_html_page(info, url)
        else:
            raise Exception(f"Unknown page file type: {info['filetype']}.")
