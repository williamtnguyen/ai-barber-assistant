# Hair0 - AI Barber Assistant

## Quick Start

### Install Dependencies
```bash
uv sync
```

### Run the System
```bash
# Interactive chat with the agent
uv run chat.py

# Start web server with React frontend (auto-populates database)
uv run main.py
```

## Features

## Architecture

### **Clean Directory Structure**
```
src/
├── core/           # Core agent and tools
│   ├── consultation-agent.py    # Main barber agent
│   └── consultation-tools.py    # Locally defined Agent tools
├── services/       # Business logic services
│   └── memory_manager.py      # Copied Mem0 layer (TODO)
├── config/         # Configuration
│   └── config.py   # All configuration constants
└── web/            # Web server
    └── server.py   # FastAPI web server
```

## Usage Examples

### **Chat Interface**
```python
from src.core.agent import create_consultation_agent

agent = create_consultation_agent()
response = agent("Suggest a nice handsome hairstyle for me")
print(response)
```

## API Endpoints

### **REST API**
- `POST /api/chat` - Chat with the beverage agent
- `POST /api/chat/stream` - Real-time streaming chat
- `GET /health` - System health check

### **Frontend**
- `/` - React web application
- `/docs` - API documentation
- Static file serving for built React app

## Technology Stack

- **Backend**: Python, FastAPI, SQLite, ChromaDB
- **AI**: Strands framework, Claude 3.5 Sonnet, Mem0
- **Frontend**: React, TypeScript, Tailwind CSS
- **Package Management**: uv

## Development

### **Key Benefits**
- **Modular design** enables easy testing of individual components
- **Clear dependencies** between modules prevent circular imports
- **Scalable architecture** supports future feature additions
- **Professional organization** follows Python packaging best practices

### **Import Structure**
```python
# Clean, organized imports
from src.core.agent import create_beverage_agent
from src.core.tools import suggest_drinks
from src.data.database import init_database
```

## Troubleshooting

### **Common Issues**
1. **Import errors**: Ensure you're using the new organized import paths
2. **Agent not responding**: Verify Strands and Claude configuration
3. **Frontend not loading**: Check if React app is built (`npm run build`)

### **System Health**
- Visit `/health` endpoint to check system status
- Check logs for detailed error information

## Success Metrics

The system is working correctly when:
- ✅ Agent suggests suitable haircuts
- ✅ System responds quickly to requests
