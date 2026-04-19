## 2025-02-28 - Hardcoded Default Webserver Password
**Vulnerability:** The webserver configuration (`parameters.py`) used a hardcoded default password (`"admin"`) for its authentication.
**Learning:** Default hardcoded passwords provide a false sense of security and leave applications vulnerable out-of-the-box, as any attacker can guess the default credentials.
**Prevention:** Always auto-generate strong random secrets/passwords by default (e.g., using `secrets.token_urlsafe(16)`) and output them, or require the user to explicitly configure authentication secrets before the application will start or expose sensitive endpoints.
