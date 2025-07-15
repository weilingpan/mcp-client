from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Update to the full absolute path to your math_server.py file
                "args": [r"C:\\Users\\zz860\\Desktop\\panpan\\mcp-demo\\server.py"],
                "transport": "stdio",
            },
            # "weather": {
            #     # Make sure you start your weather server on port 8000
            #     "url": "http://localhost:8000/mcp/",
            #     "transport": "streamable_http",
            # }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent("openai:gpt-4.1", tools)
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    print("Math response:", math_response)
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
    print("Weather response:", weather_response)

if __name__ == "__main__":
    asyncio.run(main())
