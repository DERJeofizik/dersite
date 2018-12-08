# -*- coding: utf-8 -*-

import toml

from pathlib import Path


class Config:
    def __init__(self, title, channel_id, base_url,
                 template_dir, output_dir, include_dir, deploy_dir,
                 extra_notes=None):
        self.title = title
        self.channel_id = channel_id
        self.base_url = base_url
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.include_dir = Path(include_dir)
        self.deploy_dir = Path(deploy_dir)

        if extra_notes is None:
            extra_notes = {}
        self.extra_notes = extra_notes


def load_config(filename):
    data = toml.load(filename)
    return Config(**data)
