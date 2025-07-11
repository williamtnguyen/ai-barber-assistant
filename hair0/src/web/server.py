"""
FastAPI Server for Haircut Consultation Agent

API-only backend that serves the React frontend and provides REST endpoints.
"""

import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
from src.core.consultation_agent import create_consultation_agent, get_mcp_client
import json
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Haircut Recommendation Agent API",
    description="AI-powered haircut consultant",
    version="1.0.0",
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hair_consultation_agent = create_consultation_agent()


# Pydantic models
class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None


# API Routes
@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat with the haircut agent."""
    try:
        with get_mcp_client():
            response = hair_consultation_agent(message.message)
            return ChatResponse(response=str(response), success=True)
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return ChatResponse(response="", success=False, error=str(e))


@app.post("/api/chat/stream")
async def chat_stream(message: ChatMessage):
    """Stream chat response from the haircut agent."""

    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            # Use the agent's streaming capability if available
            try:
                with get_mcp_client():
                    # Try to use stream_async if available
                    agent_stream = hair_consultation_agent.stream_async(message.message)

                    async for event in agent_stream:
                        if "data" in event:
                            # Stream text chunks as they're generated
                            chunk = {
                                "type": "text",
                                "content": event["data"],
                                "done": False,
                            }
                            yield f"data: {json.dumps(chunk)}\n\n"
                        elif "current_tool_use" in event and event["current_tool_use"].get(
                            "name"
                        ):
                            # Stream tool usage information
                            chunk = {
                                "type": "tool",
                                "content": f"Using tool: {event['current_tool_use']['name']}",
                                "additional wtf": f"{event}",
                                "done": False,
                            }
                            yield f"data: {json.dumps(chunk)}\n\n"

                    # Send completion signal
                    chunk = {"type": "done", "content": "", "done": True}
                    yield f"data: {json.dumps(chunk)}\n\n"

            except AttributeError:
                # Fallback: simulate streaming by chunking the response
                response = hair_consultation_agent(message.message)
                response_text = str(response)

                # Split response into chunks for streaming effect
                chunk_size = 20
                words = response_text.split()

                for i in range(0, len(words), chunk_size):
                    chunk_words = words[i : i + chunk_size]
                    chunk_text = " ".join(chunk_words)

                    chunk = {
                        "type": "text",
                        "content": chunk_text
                        + (" " if i + chunk_size < len(words) else ""),
                        "done": False,
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"

                    # Add small delay for streaming effect
                    await asyncio.sleep(0.1)

                # Send completion signal
                chunk = {"type": "done", "content": "", "done": True}
                yield f"data: {json.dumps(chunk)}\n\n"

        except Exception as e:
            logger.error(f"Error in streaming chat: {e}")
            error_chunk = {"type": "error", "content": f"Error: {str(e)}", "done": True}
            yield f"data: {json.dumps(error_chunk)}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        },
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "hair_consultation_agent_initialized": hair_consultation_agent is not None,
        "version": "1.0.0",
    }


# Serve React app static files
frontend_build_path = Path(__file__).parent.parent / "frontend" / "build"

if frontend_build_path.exists():
    # Mount static files for JS/CSS bundles and public assets
    app.mount(
        "/static",
        StaticFiles(directory=str(frontend_build_path / "static")),
        name="static",
    )

    @app.get("/")
    async def serve_react_app():
        """Serve the React app."""
        return FileResponse(str(frontend_build_path / "index.html"))

    @app.get("/{path:path}")
    async def serve_react_routes(path: str):
        """Serve React app for all other routes (SPA routing)."""
        # Check if it's an API route
        if path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")

        # Serve React app for all other routes
        return FileResponse(str(frontend_build_path / "index.html"))
else:

    @app.get("/")
    async def development_message():
        """Development message when React app is not built."""
        return {
            "message": "Haircut Consultant API is running!",
            "note": "React frontend not built yet. Run 'npm run build' in the frontend directory.",
            "api_docs": "/docs",
            "health": "/health",
        }
