# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from . import utils


class WebsiteCreator:
    """General class for website creation"""
    def __init__(self, conf, common_data=None):
        super().__init__()
        self.conf = conf
        self.env = Environment(
            loader=FileSystemLoader(str(self.conf.template_dir)),
            autoescape=select_autoescape(["html", "xml"]))
        self.env.filters["regex_replace"] = utils.regex_replace

        if common_data is None:
            common_data = {}
        self.common_data = common_data
        self.common_data["sitetitle"] = self.conf.title
        self.common_data["base_url"] = self.conf.base_url

    def render_to_file(self, filename, target_filename, **data):
        """Render template using data"""
        template = self.env.get_template(filename)
        self.render_template(template, target_filename, **data)

    def render_html_page(self, page_info, target_filename):
        template = self.env.from_string(page_info["content"])
        self.render_template(template, target_filename,
                             authors=self.conf.authors,
                             **page_info)

    def render_template(self, template, target_filename, **data):
        output = template.render(**self.common_data, **data)
        with open(target_filename, "w") as f:
            f.write(output)
