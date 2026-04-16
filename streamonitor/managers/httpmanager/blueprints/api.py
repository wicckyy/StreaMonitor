import json
import os
from itertools import islice
from typing import cast, Union
from flask import Blueprint, current_app, Response, request, render_template, make_response, send_from_directory
from streamonitor.managers.httpmanager.auth import login_required
from streamonitor.bot import Bot, LOADED_SITES
from streamonitor.enums import Status
from streamonitor.managers.httpmanager.models import InvalidStreamer
from streamonitor.managers.outofspace_detector import OOSDetector
from streamonitor.utils import human_file_size
from streamonitor.managers.httpmanager.mappers import web_status_lookup
from streamonitor.managers.httpmanager.utils import confirm_deletes, streamer_list, get_streamer_context, set_streamer_list_cookies, get_recording_query_params
from parameters import WEB_LIST_FREQUENCY, WEB_STATUS_FREQUENCY

def get_api_blueprint(self):
    api_bp = Blueprint('api', __name__)

    @api_bp.route('/api/basesettings')
    @login_required
    def apiBaseSettings():
        json_sites = {}
        for site in LOADED_SITES:
            json_sites[site.siteslug] = site.site
        json_status = {}
        for status in Status:
            json_status[status.value] = Bot.status_messages[status]
        return Response(json.dumps({
            "sites": json_sites,
            "status": json_status,
        }), mimetype='application/json')

    @api_bp.route('/api/data')
    @login_required
    def apiData():
        json_streamer = []
        for streamer in self.streamers:
            json_stream = {
                "site": streamer.siteslug,
                "running": streamer.running,
                "recording": streamer.recording,
                "sc": streamer.sc.value,
                "status": streamer.status(),
                "url": streamer.url,
                "username": streamer.username
            }
            json_streamer.append(json_stream)
        return Response(json.dumps({
            "streamers": json_streamer,
            "freeSpace": {
                "percentage": str(round(OOSDetector.free_space(), 3)),
                "absolute": human_file_size(OOSDetector.space_usage().free)
            }
        }), mimetype='application/json')

    @api_bp.route('/api/command')
    @login_required
    def execApiCommand():
        return self.execCmd(request.args.get("command"))



    return api_bp
