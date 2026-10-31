import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    # Support WispByte and PaaS dynamic port allocation (SERVER_PORT or PORT)
    port_env = os.environ.get("SERVER_PORT") or os.environ.get("PORT")
    port = int(port_env) if port_env and port_env.isdigit() else settings.API_PORT
    host = os.environ.get("SERVER_IP", settings.API_HOST)

    print(f"🚀 Starting DevUpward Showcase Server on {host}:{port}...")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
    )
