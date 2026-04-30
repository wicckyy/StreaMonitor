## 2024-05-24 - [Missing Authorization on Web Endpoints]
**Vulnerability:** Found `get_video` (which sends local files via `send_from_directory`) and `clear_modal` routes were missing the `@login_required` decorator, potentially exposing user data or allowing unauthorized access to state-altering actions.
**Learning:** Any new or modified Flask routes in `streamonitor/managers/httpmanager/httpmanager.py`, whether exposing sensitive media/data or performing state-altering actions, must explicitly include the custom `@login_required` decorator to prevent unauthorized access.
**Prevention:** Always verify that every route accessing sensitive data or capable of modifying server state is protected with `@login_required` unless it is explicitly intended for public access without authentication.
