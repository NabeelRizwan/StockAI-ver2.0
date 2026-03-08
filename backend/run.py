import uvicorn
import os
import sys

# Resolve the StockAI root (parent of backend/)
_STOCKAI_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add it to sys.path so "backend.app.main" resolves correctly
if _STOCKAI_ROOT not in sys.path:
    sys.path.insert(0, _STOCKAI_ROOT)

if __name__ == "__main__":
    # Change cwd to StockAI root for consistent path resolution
    os.chdir(_STOCKAI_ROOT)
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)
