# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import utils


class WebsiteCreator:
    """General class for website creation"""
    def __init__(self, conf):
        super().__init__()
        self.conf = conf
        self.env = Environment(
            loader=FileSystemLoader(str(self.conf.template_dir)),
            autoescape=select_autoescape(["html", "xml"]))
        self.env.filters["regex_replace"] = utils.regex_replace

    def render_to_file(self, filename, target_filename, **data):
        """Render template using data"""
        if len(data) == 0:
            data = {}

        data["sitetitle"] = self.conf.title
        data["base_url"] = self.conf.base_url

        template = self.env.get_template(filename)
        output = template.render(**data)
        with open(target_filename, "w") as f:
            f.write(output)
