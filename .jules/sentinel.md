## 2025-04-21 - Unauthenticated Video Access
**Vulnerability:** The `/video/<user>/<site>/<path:filename>` endpoint in `streamonitor/managers/httpmanager/httpmanager.py` lacked the `@login_required` decorator, allowing unauthenticated access to video files.
**Learning:** Even if most API and UI endpoints are properly authenticated, static file delivery or direct media access endpoints can be easily overlooked.
**Prevention:** Ensure all routes that expose sensitive data or media files have authentication decorators explicitly applied during code review.
