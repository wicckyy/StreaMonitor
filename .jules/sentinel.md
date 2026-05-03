## 2024-05-03 - Missing Authentication on Video Endpoint
**Vulnerability:** The `/video/<user>/<site>/<path:filename>` endpoint and `/clear` endpoint in `streamonitor/managers/httpmanager/httpmanager.py` are missing the `@login_required` decorator, potentially exposing recorded videos to unauthorized access and unauthenticated clears.
**Learning:** Even though most endpoints have `@login_required`, it's easy to miss it when adding new ones, especially for static file serving.
**Prevention:** Ensure every route that serves sensitive data or modifies state is explicitly decorated with `@login_required`.
