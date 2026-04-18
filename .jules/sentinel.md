# Sentinel Journal

## 2023-10-27 - Unauthenticated Video Endpoint
**Vulnerability:** The `/video/<user>/<site>/<path:filename>` endpoint in `streamonitor/managers/httpmanager/httpmanager.py` does not require authentication (`@login_required`), allowing anyone with access to the web server port to view/download recorded videos without credentials.
**Learning:** This is a significant data leakage issue. Since the web server might be exposed, leaving endpoints unprotected can lead to unauthorized access to all recorded streams.
**Prevention:** Always verify that all sensitive data endpoints are protected by appropriate authentication/authorization decorators like `@login_required` unless they are explicitly meant to be public.

## 2023-10-27 - Path Traversal Vulnerability
**Vulnerability:** The `get_video` endpoint uses `send_from_directory(os.path.abspath(streamer.outputFolder), filename)`, which is designed to prevent path traversal as it validates the requested path is within the directory, however we need to make sure the streamer object isn't somehow crafted to allow traversal. However, if `send_from_directory` is safe, then this is mostly an authentication issue.
**Learning:** `send_from_directory` in Flask is safe against directory traversal by default, but combined with the missing authentication, the videos are fully exposed.
