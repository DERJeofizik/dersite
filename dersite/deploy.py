# -*- coding: utf-8 -*-

import os
from . import utils
import datetime


def deploy(conf):
    print("Updating files")
    utils.copy_files(str(conf.output_dir / "*"), conf.deploy_dir)
    os.chdir(conf.deploy_dir)
    today = datetime.datetime.today()
    commit_command = f"git commit -am '{today}'"
    print(commit_command)
    os.system(commit_command)
    push_command = "git push origin master"
    print(push_command)
    os.system(push_command)
