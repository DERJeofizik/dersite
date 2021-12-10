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
