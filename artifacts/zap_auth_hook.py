"""ZAP baseline hook — injects an Authorization: Bearer <token> header
on every outgoing request so ZAP can scan authenticated endpoints.

Reads the token from the ZAP_AUTH_TOKEN env var (passed to the ZAP
container). Silently falls back to an unauthenticated scan if the var
is empty, so local runs without secrets still work.
"""

import os


def zap_started(zap, target):
    token = os.environ.get("ZAP_AUTH_TOKEN", "")
    if not token:
        print("[zap_auth_hook] ZAP_AUTH_TOKEN empty — scanning unauthenticated")
        return
    zap.replacer.add_rule(
        description="inject-bearer",
        enabled=True,
        matchtype="REQ_HEADER",
        matchregex=False,
        matchstring="Authorization",
        replacement=f"Bearer {token}",
        initiators="",
    )
    print("[zap_auth_hook] Authorization: Bearer <service_role> injected")
