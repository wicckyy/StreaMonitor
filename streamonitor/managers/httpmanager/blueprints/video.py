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

def get_video_blueprint(self):
    video_bp = Blueprint('video', __name__)

    @video_bp.route('/recordings/<user>/<site>', methods=['GET'])
    @login_required
    def recordings(user, site):
        video = request.args.get("play_video")
        sort_by_size = bool(request.args.get("sorted", False))
        streamer = cast(Union[Bot, None], self.getStreamer(user, site))
        streamer.cache_file_list()
        context = get_streamer_context(streamer, sort_by_size, video, request.headers.get('User-Agent'))
        status_code = 500 if context['has_error'] else 200
        if video is None and streamer.recording and len(context['videos']) > 1:
            # It might not always be safe to grab the biggest file if sorting by size, but good enough for now
            video_index = 0 if sort_by_size else 1
            context['video_to_play'] = next(islice(context['videos'].values(), video_index, video_index + 1))
        elif video is None and len(context['videos']) > 0 and not streamer.recording:
            context['video_to_play'] = next(islice(context['videos'].values(), 0, 1))
        return render_template('recordings.html.jinja', **context), status_code

    @video_bp.route('/video/<user>/<site>/<path:filename>', methods=['GET'])
    def get_video(user, site, filename):
        streamer = cast(Union[Bot, None], self.getStreamer(user, site))
        return send_from_directory(
            os.path.abspath(streamer.outputFolder),
            filename
        )

    @video_bp.route('/videos/watch/<user>/<site>/<path:play_video>', methods=['GET'])
    @login_required
    def watch_video(user, site, play_video):
        sort_by_size = bool(request.args.get("sorted", False))
        streamer = cast(Union[Bot, None], self.getStreamer(user, site))
        context = get_streamer_context(streamer, sort_by_size, play_video, request.headers.get('User-Agent'))
        status_code = 500 if context['video_to_play'] is None or context['has_error'] else 200
        response = make_response(render_template('recordings_content.html.jinja', **context), status_code)
        query_param = get_recording_query_params(sort_by_size, play_video)
        response.headers['HX-Replace-Url'] = f"/recordings/{user}/{site}{query_param}"
        return response

    @video_bp.route('/videos/<user>/<site>', methods=['GET'])
    @login_required
    def sort_videos(user, site):
        streamer = cast(Union[Bot, None], self.getStreamer(user, site))
        sort_by_size = bool(request.args.get("sorted", False))
        play_video = request.args.get("play_video", None)
        context = get_streamer_context(streamer, sort_by_size, play_video, request.headers.get('User-Agent'))
        status_code = 500 if context['has_error'] else 200
        response = make_response(render_template('video_list.html.jinja', **context), status_code)
        query_param = get_recording_query_params(sort_by_size, play_video)
        response.headers['HX-Replace-Url'] = f"/recordings/{user}/{site}{query_param}"
        return response

    @video_bp.route('/videos/<user>/<site>/<path:filename>', methods=['DELETE'])
    @login_required
    def delete_video(user, site, filename):
        streamer = cast(Union[Bot, None], self.getStreamer(user, site))
        sort_by_size = bool(request.args.get("sorted", False))
        play_video = request.args.get("play_video", None)
        context = get_streamer_context(streamer, sort_by_size, play_video, request.headers.get('User-Agent'))
        status_code = 200
        match = context['videos'].pop(filename, None)
        if match is not None:
            try:
                os.remove(match.abs_path)
                streamer.cache_file_list()
                context['total_size'] = context['total_size'] - match.filesize
                if context['video_to_play'] is not None and filename == context['video_to_play'].filename:
                    context['video_to_play'] = None
            except Exception as e:
                status_code = 500
                context['has_error'] = True
                context['recordings_error_message'] = repr(e)
                self.logger.error(e)
        else:
            status_code = 404
            context['has_error'] = True
            context['recordings_error_message'] = f'Could not find {filename}, so no file removed'
        response = make_response(render_template('video_list.html.jinja', **context), status_code)
        query_param = get_recording_query_params(sort_by_size, play_video)
        response.headers['HX-Replace-Url'] = f"/recordings/{user}/{site}{query_param}"
        return response



    return video_bp
