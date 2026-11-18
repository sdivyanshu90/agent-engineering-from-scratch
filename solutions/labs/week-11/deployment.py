"""Reference: validate secret presence without exposing its value."""
from pathlib import PurePosixPath


def deployment_contract(environment):
    token = environment.get("FORGEAGENT_TOKEN")
    database = environment.get("FORGEAGENT_DATABASE", "/data/forgeagent.sqlite3")
    if not token:
        raise ValueError("token required")
    path = PurePosixPath(database)
    if not path.is_absolute() or path.parent == PurePosixPath("/"):
        raise ValueError("database must be inside a persistent data directory")
    return {"token_configured": True, "database": str(path),
            "topology": "single_host_sqlite", "nonroot_required": True,
            "health_path": "/health"}
