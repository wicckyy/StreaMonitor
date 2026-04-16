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

def get_action_blueprint(self):
    action_bp = Blueprint('action', __name__)

    @action_bp.route("/add", methods=['POST'])
    @login_required
    def add():
        user = request.form["username"]
        site = request.form["site"]
        update_site_options = site not in map(lambda x: x.site, self.streamers)
        toast_status = "success"
        status_code = 200
        streamer = self.getStreamer(user, site)
        res = self.do_add(streamer, user, site)
        streamers, filter_context = streamer_list(self.streamers, request)
        if res == 'Streamer already exists' or res == "Missing value(s)" or res == "Failed to add":
            toast_status = "error"
            status_code = 500
        context = {
            'streamers': streamers,
            'unique_sites': set(map(lambda x: x.site, self.streamers)),
            'update_filter_site_options': update_site_options,
            'refresh_freq': WEB_LIST_FREQUENCY,
            'toast_status': toast_status,
            'toast_message': res,
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        } | filter_context
        return render_template('streamers_result.html.jinja', **context), status_code

    @action_bp.route("/recording/nav/<user>/<site>", methods=['GET'])
    @login_required
    def get_streamer_navbar(user, site):
        streamer = self.getStreamer(user, site)
        sort_by_size = bool(request.args.get("sorted", False))
        play_video = request.args.get("play_video", None)
        previous_state = request.args.get("prev_state", False)
        streamer_context = {}
        # need this from the UI perspective to know whether to update due to polling windows
        if previous_state != streamer.sc:
            streamer_context = get_streamer_context(
                streamer, sort_by_size, play_video, request.headers.get('User-Agent'))
        status_code = 200
        has_error = False
        if streamer is None:
            status_code = 500
            streamer = InvalidStreamer(user, site)
            has_error = True
        context = {
            **streamer_context,
            'update_content': False if len(streamer_context) == 0 else True,
            'streamer': streamer,
            'has_error': has_error,
            'refresh_freq': WEB_STATUS_FREQUENCY,
        }
        return render_template('streamer_nav_bar.html.jinja', **context), status_code

    @action_bp.route("/streamer-info/<user>/<site>", methods=['GET'])
    @login_required
    def get_streamer_info(user, site):
        streamer = self.getStreamer(user, site)
        res = None
        status_code = 200
        has_error = False
        if streamer is None:
            status_code = 500
            res = f"Could not get info for {user} on site {site}"
            has_error = True
        streamer.cache_file_list()
        context = {
            'streamer': streamer,
            'streamer_has_error': has_error,
            'streamer_error_message': res,
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        }
        return render_template('streamer_record.html.jinja', **context), status_code

    @action_bp.route("/remove/<user>/<site>", methods=['DELETE'])
    @login_required
    def remove_streamer(user, site):
        streamer = self.getStreamer(user, site)
        res = self.do_remove(streamer, user, site)
        status_code = 204
        if res == "Failed to remove streamer" or res == "Streamer not found":
            status_code = 404
            context = {
                'streamer_error_message': res,
            }
            response = make_response(render_template('streamer_record_error.html.jinja', **context), status_code)
            response.headers['HX-Retarget'] = "#error-container"
            return response
        return '', status_code

    @action_bp.route("/clear", methods=['DELETE'])
    def clear_modal():
        return '', 204

    @action_bp.route("/toggle/<user>/<site>", methods=['PATCH'])
    @login_required
    def toggle_streamer(user, site):
        streamer = self.getStreamer(user, site)
        status_code = 500
        res = "Streamer not found"
        has_error = True
        if streamer is None:
            status_code = 500
        elif streamer.running:
            res = self.do_stop(streamer, user, site)
        else:
            res = self.do_start(streamer, user, site)
        if res == "OK":
            has_error = False
            status_code = 200
        context = {
            'streamer': streamer,
            'streamer_has_error': has_error,
            'streamer_error_message': res,
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        }
        return render_template('streamer_record.html.jinja', **context), status_code

    @action_bp.route("/toggle/<user>/<site>/recording", methods=['PATCH'])
    @login_required
    def toggle_streamer_recording_page(user, site):
        streamer = self.getStreamer(user, site)
        status_code = 500
        res = "Streamer not found"
        has_error = True
        if streamer is None:
            status_code = 500
        elif streamer.running:
            res = self.do_stop(streamer, user, site)
        else:
            res = self.do_start(streamer, user, site)
        if res == "OK":
            has_error = False
            status_code = 200
        context = {
            'streamer': streamer,
            'streamer_has_error': has_error,
            'streamer_error_message': res,
        }
        return render_template('streamer_toggle.html.jinja', **context), status_code

    @action_bp.route("/start/streamers", methods=['PATCH'])
    @login_required
    def start_streamers():
        status_code = 500
        toast_status = "error"
        streamers, filter_context = streamer_list(self.streamers, request)
        res = ""
        error_message = ""
        try:
            if not filter_context.get('filtered') or len(streamers) == len(self.streamers):
                res = self.do_start(None, '*', None)
                if res == "Started all":
                    status_code = 200
                    toast_status = "success"
            else:
                error = []
                if len(streamers) > 0:
                    for streamer in streamers:
                        partial_res = self.do_start(streamer, None, None)
                        if partial_res != "OK":
                            error.append(streamer.username)
                    res = "Started All Shown"
                else:
                    res = 'no matching streamers'
                if len(error) > 0:
                    toast_status = "warning"
                    res = "Some Failed to Start"
                    error_message = "The following streamers failed to start:\n " + '\n'.join(error)
                else:
                    status_code = 200
                    toast_status = "success"
        except Exception as e:
            self.logger.warning(e)
            res = str(e)
        context = {
            'streamers': streamers,
            'refresh_freq': WEB_LIST_FREQUENCY,
            'toast_status': toast_status,
            'toast_message': res,
            'error_message': error_message,
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        } | filter_context
        return render_template('streamers_result.html.jinja', **context), status_code

    @action_bp.route("/stop/streamers", methods=['PATCH'])
    @login_required
    def stop_streamers():
        status_code = 500
        toast_status = "error"
        streamers, filter_context = streamer_list(self.streamers, request)
        res = ""
        error_message = ""
        try:
            if not filter_context.get('filtered') or len(streamers) == len(self.streamers):
                res = self.do_stop(None, '*', None)
                if res == "Stopped all":
                    status_code = 200
                    toast_status = "success"
            else:
                error = []
                if len(streamers) > 0:
                    for streamer in streamers:
                        partial_res = self.do_stop(streamer, None, None)
                        if partial_res != "OK":
                            error.append(streamer.username)
                    res = "Stopped All Shown"
                else:
                    res = 'no matching streamers'
                if len(error) > 0:
                    toast_status = "warning"
                    res = "Some Failed to Stop"
                    error_message = "The following streamers failed to stop:\n" + '\n'.join(error)
                else:
                    status_code = 200
                    toast_status = "success"
        except Exception as e:
            self.logger.warning(e)
            res = str(e)

        context = {
            'streamers': streamers,
            'refresh_freq': WEB_LIST_FREQUENCY,
            'toast_status': toast_status,
            'toast_message': res,
            'error_message': error_message,
            'confirm_deletes': confirm_deletes(request.headers.get('User-Agent')),
        } | filter_context
        return render_template('streamers_result.html.jinja', **context), status_code



    return action_bp
