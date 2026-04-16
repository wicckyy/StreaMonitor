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

def get_ui_blueprint(self):
    ui_bp = Blueprint('ui', __name__)

    @ui_bp.route('/dashboard')
    @login_required
    def mainSite():
        return current_app.send_static_file('index.html')


    @ui_bp.route('/', methods=['GET'])
    @login_required
    def status():
        usage = OOSDetector.space_usage()
        streamers, filter_context = streamer_list(self.streamers, request)
        context = {
            'streamers': streamers,
            'sites': self.loaded_site_names,
            'unique_sites': set(map(lambda x: x.site, self.streamers)),
            'streamer_statuses': web_status_lookup,
            'free_space': human_file_size(usage.free),
            'total_space': human_file_size(usage.total),
            'percentage_free': round(usage.free / usage.total * 100, 3),
            'refresh_freq': WEB_LIST_FREQUENCY,
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        } | filter_context
        return render_template('index.html.jinja', **context)

    @ui_bp.route('/refresh/streamers', methods=['GET'])
    @login_required
    def refresh_streamers():
        streamers, filter_context = streamer_list(self.streamers, request)
        context = {
            'streamers': streamers,
            'sites': LOADED_SITES,
            'refresh_freq': WEB_LIST_FREQUENCY,
            'toast_status': "hide",
            'toast_message': "",
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        } | filter_context
        response = make_response(render_template('streamers_result.html.jinja', **context))
        set_streamer_list_cookies(filter_context, request, response)
        return response



    return ui_bp
