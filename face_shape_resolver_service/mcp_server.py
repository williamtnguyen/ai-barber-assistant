from fastmcp import FastMCP
from media_pipe_face_shape_descriptor import describe_face_shape_localhost_mcp_tool

"""
FastMCP Tool Service for Face Descriptions
"""

mcp = FastMCP(
    name="FaceDescriptorMCPTool",
    instructions="Use this Face Descriptor tool when there is an image of a hair client's face whose shape needs to be described.",
)

@mcp.tool()
def describe_face_shape_tool(image_path: str):
    return describe_face_shape_localhost_mcp_tool(image_path)
