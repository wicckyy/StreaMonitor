
## 2024-04-17 - [Remove Hardcoded default password from config]
**Vulnerability:** A hardcoded default password `"admin"` was in `parameters.py`.
**Learning:** The application had a hardcoded default password for the admin user which is poor security practice because any default deployment will have the same exact password.
**Prevention:** Hardcoded static default passwords should be replaced with dynamically securely generated random passwords printed on startup, or prompt the user for password on startup, or just no auth. In this case, we replaced it with a securely generated `secrets.token_urlsafe(16)` password which prints out securely in the logs on startup unless overridden. Empty string can still explicitly be passed in to disable auth.
