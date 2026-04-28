## 2024-05-01 - [Hardcoded Web Interface Password Removed]
**Vulnerability:** The web server interface password in `parameters.py` was hardcoded to "admin" by default (`WEBSERVER_PASSWORD = env.str("STRMNTR_PASSWORD", "admin")`).
**Learning:** Default hardcoded passwords in configuration files expose applications to unauthorized access if users deploy them without changing the defaults.
**Prevention:** Always default to auto-generating secure, random passwords (e.g., using `secrets.token_urlsafe()`) if a user-supplied configuration value is missing.
