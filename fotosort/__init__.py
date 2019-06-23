#!/usr/bin/env python

import argparse
from types import SimpleNamespace
import yaml
import glob
import os
import appdirs
import sys

from .ui import UI
from .controller import Controller


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', help="Directory containing the source files", required=False)
    args = parser.parse_args()

    confpath = os.path.join(appdirs.user_config_dir(), "fotosort.yaml")

    if os.path.isfile(confpath):
        with open(confpath) as stream:
            conf = SimpleNamespace(**yaml.safe_load(stream))
    else:
        conf = SimpleNamespace(
            copy_pictures=False,
            extensions=['*.jpg', '*.JPG', '*.png', '*.PNG'],
            perm_output_dirs=[],
            temp_output_prefix=os.path.expanduser('~')
        )

    controller = Controller(conf, args.location)
    ui = UI(conf, controller)

    sys.excepthook = ui.excepthook

    ui.run()

    with open(confpath, 'w') as stream:
        stream.write(yaml.safe_dump(vars(conf)))
