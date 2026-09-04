"""
Vercel Serverless Function Entry Point for ShramAI FastAPI Application.
Exposes the ASGI app instance for Vercel Python Runtime.
"""
import os
import sys
from pathlib import Path

# Set VERCEL environment flag if running under Vercel
os.environ.setdefault("VERCEL", "1")

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Ensure data directories are discoverable from root
root_dir = Path(__file__).resolve().parent.parent
os.chdir(root_dir)

from app.main import app
