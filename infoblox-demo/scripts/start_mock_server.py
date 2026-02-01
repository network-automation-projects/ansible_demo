#!/usr/bin/env python3
"""Start the mock Infoblox WAPI server."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mock_server.server import app

if __name__ == "__main__":
    print("Starting Mock Infoblox WAPI server on http://localhost:8080")
    print("Press Ctrl+C to stop")
    app.run(host="0.0.0.0", port=8080, debug=False)
