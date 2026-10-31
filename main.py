import os
import sys

# Force unbuffered output so logs appear instantly in WispByte console
os.environ["PYTHONUNBUFFERED"] = "1"
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if os.path.abspath(".") not in sys.path:
    sys.path.insert(0, os.path.abspath("."))

from app.core.config import settings
import uvicorn

if __name__ == "__main__":
    port_env = os.environ.get("SERVER_PORT") or os.environ.get("PORT")
    port = int(port_env) if port_env and port_env.isdigit() else settings.API_PORT
    host = os.environ.get("SERVER_IP", "0.0.0.0")

    print(f"🚀 Starting DevUpward Showcase Server on {host}:{port}...", flush=True)
    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=False,
    )
