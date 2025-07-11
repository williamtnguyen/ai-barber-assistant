"""
Configuration for Beverage Recommendation Agent

Self-hosted mem0 and SQLite configuration settings.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent  # Go up to src/ directory
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "beverages.db"

# Mem0 self-hosted configuration
MEM0_CONFIG = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "beverage_preferences",
            "path": str(DATA_DIR / "beer0_memory_db")
        }
    },
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "temperature": 0.2,
            "max_tokens": 20000,
        }
    },
    "embedder": {
        "provider": "aws_bedrock",
        "config": {
            "model": "amazon.titan-embed-text-v2:0",
        }
    }
}

# SQLite MCP server configuration
SQLITE_MCP_CONFIG = {
    "database_path": str(DATABASE_PATH),
    "server_name": "beverage_sqlite",
}

# Default user ID for single-user system
DEFAULT_USER_ID = "beverage_user"

# Beverage categories
BEVERAGE_CATEGORIES = ["beer", "wine", "spirits", "cocktails"]

# Rating scale
MIN_RATING = 1
MAX_RATING = 5
