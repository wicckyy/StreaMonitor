## 2024-05-XX - Missing Authentication on Video Endpoint
**Vulnerability:** Missing `@login_required` decorator on `/video/<user>/<site>/<path:filename>` endpoint and `/clear` endpoint.
**Learning:** Any endpoint serving sensitive files or performing actions should be protected, even if it feels "internal".
**Prevention:** Apply authentication to all relevant endpoints exposing user data or modifying state.
