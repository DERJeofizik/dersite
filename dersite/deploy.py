# -*- coding: utf-8 -*-

import os
from . import utils
import datetime


def run_command(command):
    print(command)
    os.system(command)


def deploy(conf):
    print("Updating files")
    utils.copy_files(str(conf.output_dir / "*"), conf.deploy_dir)
    os.chdir(conf.deploy_dir)
    run_command("git pull origin master")
    run_command("git checkout master")
    today = datetime.datetime.today()
    run_command("git add .")
    run_command(f"git commit -am '{today}'")
    run_command("git push origin master")
