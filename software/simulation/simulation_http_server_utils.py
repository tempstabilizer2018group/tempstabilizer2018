# -*- coding: utf-8 -*-
import os

import config_app

strNodeDirectory = os.path.dirname(os.path.dirname(config_app.__file__))
strNodeDataDirectory = os.path.join(strNodeDirectory, config_app.DIRECTORY_DATA)

