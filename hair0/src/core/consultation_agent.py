"""
Hairstyle Consultation Agent

An expert agent that suggests suiting hairstyles based on user face anatomy
"""

import logging
from typing import Any, List
from strands import Agent
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp import MCPClient
from strands.types.exceptions import MCPClientInitializationError
from src.core.consultation_tools import describe_face_shape, search_knowledge_base
from contextlib import contextmanager

logger = logging.getLogger(__name__)


face_shape_descriptor_http_mcp_client = MCPClient(lambda: streamablehttp_client(
    "http://localhost:8001/mcp"
))

@contextmanager
def get_mcp_client():
    with face_shape_descriptor_http_mcp_client as client:
        yield client


def create_strands_claude_agent(agent_name: str, system_prompt: str, tools: List[Any]) -> Agent:
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        system_prompt=system_prompt,
        tools=tools,
        callback_handler=None
    )
    logger.info(f"{agent_name} created successfully!!")
    logger.info(f"Available tools: {[tool.tool_name for tool in tools]}")
    return agent


def create_consultation_agent() -> Agent:
    """Create the consultation agent with expert knowledge."""

    system_prompt = """You are a world-renowned barber and hairstylist with deep knowledge of various topics, enabling you to give a client a tailored consultation and hairstyle recommendation. Those topics include:

HAIRSTYLES:
- Names: Buzzcut, Wolfcut, Textured Fringe, Edgar, Brushback, Mullet, Combover, Gentleman's
- Types: Long, Short, Connected, Disconnected
- Maintenance (effort in styling): Low, Medium, High
- Upkeep (frequency of needing to make an appointment): Low, Medium, High
- Which hairstyles are well suited with certain face shapes

FACE AND HEAD ANATOMY:
- Face shape: Round, Oblong, Square, Heart
- Head nuances: Receding hairline/balding, hair growth patterns 
- Which face shapes and head nuances are well suited with certain hairstyles

YOUR APPROACH:
1. If a query asks a general question about hairstyles, use the search_knowledge_base tool to retrieve different documents about hairstyles that the query asked about
1. If a query asks for a personal hair recommendation, you need an image of the client's face
  1a. To get the image, the user will use the UI to snap a photo of themselves, and then on the image path should be submitted as their next query
  1b. To parse the image and get a facial shape description, use the describe_face_shape tool to validate that the image was taken, and to call the face shape descriptor service to get a description
2. Once you have a face description, you should use the search_knowledge_base tool to retrieve different documents containing information about hairstyles suited for the client's face shape
3. Use those documents to choose a recommended hairstyle. Give a thoughtful response with additional context from the document.

CONVERSATION STYLE:
- Be knowledgeable but approachable
- Share interesting facts about hairstyles and face shapes
- Ask follow-up questions to better understand preferences
- Seem knowledgeable about the hair domain and empathetic to the client

TOOLS AVAILABLE:
- describe_face_shape_tool: Use the user submitted filepath prefixed with "facecapture-", suffixed with ".jpg" and call the face shape descriptor MCP tool with this input to get a face shape description
- search_knowledge_base: Retrieval tool to query a knowledge base using relevant keywords from documents matching to face shape description

The flow should be simple, understandble, and consistent. Please rely on your tools to guide you to the next step."""

    local_tools = [search_knowledge_base]

    try:
        with get_mcp_client() as mcp_client:
            face_shape_descriptor_tools = mcp_client.list_tools_sync()

            # Create the agent with local and MCP tools
            return create_strands_claude_agent("Hair Consultation Agent", system_prompt, [*local_tools, *face_shape_descriptor_tools])
    
    except MCPClientInitializationError:
        # Fallback to agent with local_tools if HTTP MCP connections can't be created
        return create_strands_claude_agent("Hair Consultation Agent", system_prompt, [*local_tools])
