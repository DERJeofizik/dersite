#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse


from dersite.download import download_channel_info
from dersite.create import create
from dersite.config import load_config
from dersite.server import run_local_server
from dersite.deploy import deploy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run")
    subparsers = parser.add_subparsers(title="command", dest="command",
                                       help="command name")
    parser_download = subparsers.add_parser(
        "download", help="Download metadata from Youtube")
    parser_download.add_argument("config_file", help="config file (toml)")
    parser_download.add_argument("output_file", help="output json filename",
                                 default="data.json")

    parser_create = subparsers.add_parser("create",
                                          help="Create the website")
    parser_create.add_argument("config_file", help="config file (toml)")
    parser_create.add_argument("data_filename", help="metadata file (json)")
    parser_create.add_argument("--base-url", "-b", default=None,
                               help="Base url (for localhost testing)")

    parser_server = subparsers.add_parser("server",
                                          help="Run local web server")
    parser_server.add_argument("config_file", help="config file (toml)")
    parser_server.add_argument("--ip", default="localhost",
                               help="localhost ip (localhost)")
    parser_server.add_argument("--port", "-p", default=8000,
                               help="localhost port (8000)")

    parser_deploy = subparsers.add_parser("deploy",
                                          help="Run deployment commands")
    parser_deploy.add_argument("config_file", help="config file (toml)")

    args = parser.parse_args()

    conf = load_config(args.config_file)
    if args.command == "download":
        download_channel_info(conf.channel_id,
                              args.output_file)
    elif args.command == "create":
        create(conf, args.data_filename, args.base_url)
    elif args.command == "server":
        run_local_server(conf, args.ip, args.port)
    elif args.command == "deploy":
        deploy(conf)
    else:
        print("No job is given.")
