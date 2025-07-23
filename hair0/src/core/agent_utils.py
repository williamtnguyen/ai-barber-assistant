import logging
from typing import Any, List
from strands import Agent

logger = logging.getLogger(__name__)


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
