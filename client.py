# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

import os
import getpass
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
os.environ["TAVILY_API_KEY"] = tavily_api_key

server_params = StdioServerParameters(
    command="python",
    args=[r"C:\\Users\\zz860\\Desktop\\panpan\\mcp-demo\\server.py"],
)

import asyncio

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            print(f"The available tools are: {len(tools)} tools")
            print("Tools:", tools)

            # Create and run the agent
            model = ChatOpenAI(model="gpt-4o-mini")
            agent = create_react_agent(model, tools)

            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            print("Agent response:", agent_response)

if __name__ == "__main__":
    asyncio.run(main())