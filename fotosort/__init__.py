#!/usr/bin/env python

import argparse
import os
import sys
from types import SimpleNamespace

import appdirs
import yaml

from .controller import Controller
from .ui import UI


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', help="Directory containing the source files", required=False)
    args = parser.parse_args()

    confpath = os.path.join(appdirs.user_config_dir(), "fotosort.yaml")

    conf_dict = {
        "copy_pictures": False,
        "extensions": ['*.jpg', '*.JPG', '*.png', '*.PNG'],
        "perm_output_dirs": [],
        "timestamp_prefix_format": "%Y_%m_%d",
        "temp_output_prefix": os.path.expanduser('~')
    }

    if os.path.isfile(confpath):
        with open(confpath) as stream:
            loaded = yaml.safe_load(stream) or {}
            conf_dict.update(loaded)

    conf = SimpleNamespace(**conf_dict)

    controller = Controller(conf, args.location)
    ui = UI(conf, controller)

    sys.excepthook = ui.excepthook

    ui.run()

    with open(confpath, 'w') as stream:
        stream.write(yaml.safe_dump(vars(conf)))
