
from typing import Any, Dict
import os

API_VER = "v1"
app_configs: Dict[str, Any] = {"title": "AutoMate API"}
if os.getenv("PY_ENV") != "development":
    app_configs["openapi_url"] = None  # hide docs in production