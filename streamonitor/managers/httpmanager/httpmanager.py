from itertools import islice
from typing import cast, Union

from flask import Flask
import os
import json
import logging

from parameters import WEBSERVER_HOST, WEBSERVER_PORT, WEBSERVER_SKIN
import streamonitor.log as log
from streamonitor.bot import Bot, LOADED_SITES
from streamonitor.enums import Status
from streamonitor.manager import Manager
from streamonitor.utils import human_file_size

from .filters import status_icon, status_text

from .blueprints.api import get_api_blueprint
from .blueprints.ui import get_ui_blueprint
from .blueprints.video import get_video_blueprint
from .blueprints.action import get_action_blueprint


class HTTPManager(Manager):
    def __init__(self, streamers):
        super().__init__(streamers)
        self.logger = log.Logger("manager")
        self.loaded_site_names = [site.site for site in LOADED_SITES]
        self.loaded_site_names.sort()

        skin = WEBSERVER_SKIN
        if skin in os.listdir(os.path.join(os.path.dirname(__file__), 'skins')):
            self.skin = skin
        else:
            raise ValueError(f'Invalid skin name: {skin}')

    def run(self):
        app = Flask(
            __name__,
            template_folder=f'skins/{self.skin}/templates'
        )
        
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.disabled = True

        app.add_template_filter(human_file_size, name='tohumanfilesize')
        app.add_template_filter(status_icon, name='status_icon_class')
        app.add_template_filter(status_text, name='status_text')

        # Register blueprints
        app.register_blueprint(get_api_blueprint(self))
        app.register_blueprint(get_ui_blueprint(self))
        app.register_blueprint(get_video_blueprint(self))
        app.register_blueprint(get_action_blueprint(self))

        app.run(host=WEBSERVER_HOST, port=WEBSERVER_PORT)
