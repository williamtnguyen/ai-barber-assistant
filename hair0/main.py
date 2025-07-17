#!/usr/bin/env python3
"""
Hair0 - AI Haircut Consultant Main Entry Point

Starts the FastAPI server for the haircut recommendation system.
"""

import sys
import os
from pathlib import Path
import base64
import uvicorn
 
# Get keys for your project from the project settings page: https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-4f815fc0-c06a-41f9-bc14-5fd6d5f91af2"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-918ea3ad-53d6-4a92-a788-0597bc5f022f" 
os.environ["LANGFUSE_HOST"] = "http://localhost:3000" # 🇪🇺 EU region (default)
 
# Build Basic Auth header.
LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
).decode()
 
# Configure OpenTelemetry endpoint & headers
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get("LANGFUSE_HOST") + "/api/public/otel/v1/traces"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

os.environ["ANONYMIZED_TELEMETRY"] = "FALSE"
os.environ["MEM0_TELEMETRY"] = "False"

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the server
from src.web.server import app


if __name__ == "__main__":    
    print("🍷 Starting Hair0 - AI Haircut Consultant 💇‍♂️")
    print("=" * 50)
    
    print("\n🌐 Starting web server...")
    print("Server running on: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
        )
    except KeyboardInterrupt:
        print("\n🍻 Thanks for using Hair0! Cheers!")
