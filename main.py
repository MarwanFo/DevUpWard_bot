import os
import sys

# Force unbuffered output so logs appear instantly in WispByte console
os.environ["PYTHONUNBUFFERED"] = "1"
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass

# Add .local/lib/python*/site-packages if present (Pterodactyl / Wispbyte container support)
local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".local"))
if os.path.exists(local_dir):
    for root, dirs, files in os.walk(local_dir):
        if os.path.basename(root) == "site-packages":
            if root not in sys.path:
                sys.path.insert(0, root)

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from app.core.config import settings
except ImportError:
    from backend.app.core.config import settings

import uvicorn


def start():
    try:
        port_env = os.environ.get("SERVER_PORT") or os.environ.get("PORT")
        port = int(port_env) if port_env and port_env.isdigit() else settings.API_PORT
        host = os.environ.get("SERVER_IP", "0.0.0.0")

        print(f"🚀 Starting DevUpward Showcase Server on {host}:{port}...", flush=True)
        from app.main import app
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,
        )
    except Exception as e:
        print(f"💥 Fatal error during server startup: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    start()
