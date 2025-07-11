from web_server import app
from mcp_server import mcp as face_descriptor_mcp
import sys


def start_web_server():
    print("\n🌐 Starting web server...")
    print("Server running on: http://localhost:8001")
    print("=" * 50)

    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
        )
    except KeyboardInterrupt:
        print("\n🍻 Thanks for using Face Descriptor Service! Cheers!")


def start_mcp_server():
    print("\n🌐 Starting MCP server...")
    print("Server running!!")
    print("=" * 50)

    face_descriptor_mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8001,
        path="/mcp",
        log_level="debug",
    )


if __name__ == "__main__":
    import uvicorn
    
    print("🍷 Starting Face Descriptor Service!!")
    print("=" * 50)

    server_protocol = sys.argv[1] if (len(sys.argv) == 2 and sys.argv[0] == "main.py") else input("Would you like to start this service as either:\n1. HTTP Web Server\n2. MCP Tool Service\n????\n")

    match server_protocol:
        case "1" | "web" | "Web":
            start_web_server()
        case "2" | "mcp" | "MCP":
            start_mcp_server()
        case _:
            print("Unknown server protocol type selected.")
