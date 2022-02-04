#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import http.server
import socketserver


def run_local_server(conf, ip, port):
    Handler = http.server.SimpleHTTPRequestHandler
    os.chdir(conf.output_dir)

    with socketserver.TCPServer((ip, port), Handler) as httpd:
        print(f"Running Web Server at http://{ip}:{port}")
        httpd.serve_forever()


def run_dev_server(conf, ip, port):
    from livereload import Server, shell
    server = Server()
    recreate_command = f"./run.py create -b http://{ip}:{port}"
    server.watch("dersite", shell(recreate_command))
    server.watch(conf.template_dir, shell(recreate_command))
    server.watch(conf.pages_dir, shell(recreate_command))
    server.watch("config.toml", shell(recreate_command))
    server.serve(host=ip, port=port, root=conf.output_dir)
