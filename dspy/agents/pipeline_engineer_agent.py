"""
DSPy Pipeline Engineer Agent for Keboola MCP Server

A generalized, modular pipeline engineer agent that can handle any type of data pipeline
design and engineering request dynamically using the Keboola MCP Server tools.
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import dspy


class PipelineEngineeringSignature(dspy.Signature):
    """
    You are an expert data engineer with access to comprehensive Keboola data platform tools.
    You can design pipelines, create transformations, manage flows, and orchestrate data processing.
    
    Your approach should be:
    1. Understand the pipeline requirements thoroughly
    2. Analyze available data sources and destinations
    3. Design efficient, scalable pipeline architectures
    4. Use appropriate tools to implement components and flows
    5. Apply data engineering best practices
    6. Ensure data quality and reliability
    7. Provide clear implementation plans and documentation
    
    Always consider scalability, maintainability, and monitoring in your designs.
    """
    
    engineering_request: str = dspy.InputField(
        desc="The user's pipeline engineering request, requirements, or problem to solve"
    )
    
    engineering_result: str = dspy.OutputField(
        desc="Comprehensive engineering solution with architecture, implementation plan, and recommendations"
    )


class KeboolaPipelineEngineer:
    """
    A modular, generalized pipeline engineer agent that can handle any data engineering task
    using Keboola MCP Server tools dynamically.
    """
    
    def __init__(self, model: str = "openai/o3"):
        """
        Initialize the pipeline engineer agent.
        
        Args:
            model: The language model to use for engineering tasks
        """
        # Configure DSPy with the specified language model
        # O3 reasoning models require specific parameters
        if "o3" in model.lower():
            dspy.configure(lm=dspy.LM(model, temperature=1.0, max_tokens=20000))
        else:
            dspy.configure(lm=dspy.LM(model))
        
        # Keboola MCP Server parameters
        self.server_params = StdioServerParameters(
            command="uvx",
            args=["--from", "keboola-mcp-server@1.0.0", "keboola-mcp-server"],
            env={
                "KBC_STORAGE_API_URL": os.getenv("KBC_STORAGE_API_URL"),
                "KBC_STORAGE_TOKEN": os.getenv("KBC_STORAGE_TOKEN"),
                "KBC_WORKSPACE_SCHEMA": os.getenv("KBC_WORKSPACE_SCHEMA", "")
            }
        )
        
        self.tools = []
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the MCP connection and load available tools."""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # List available tools
                tools_response = await session.list_tools()
                
                # Convert MCP tools to DSPy tools
                self.tools = []
                for tool in tools_response.tools:
                    dspy_tool = dspy.Tool.from_mcp_tool(session, tool)
                    self.tools.append(dspy_tool)
                
                self._initialized = True
                print(f"✅ Initialized Keboola Pipeline Engineer with {len(self.tools)} tools")
    
    async def design_pipeline(self, request: str) -> str:
        """
        Design and implement data pipelines based on any user request.
        
        This is the main method that handles all types of pipeline engineering requests
        dynamically using the available Keboola tools.
        
        Args:
            request: The user's pipeline engineering request or requirements
            
        Returns:
            Engineering solution with architecture and implementation plan
        """
        if not self._initialized:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Recreate tools for this session
                tools_response = await session.list_tools()
                session_tools = []
                for tool in tools_response.tools:
                    dspy_tool = dspy.Tool.from_mcp_tool(session, tool)
                    session_tools.append(dspy_tool)
                
                # Create ReAct agent for this session
                agent = dspy.ReAct(PipelineEngineeringSignature, tools=session_tools)
                
                # Execute the engineering task
                result = await agent.acall(engineering_request=request)
                return result.engineering_result
    
    def get_available_tools(self) -> List[str]:
        """
        Get a list of available tool names for reference.
        
        Returns:
            List of tool names that can be used for pipeline engineering
        """
        if not self._initialized:
            return []
        return [tool.name for tool in self.tools]
    
    def get_tool_info(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about available tools.
        
        Args:
            tool_name: Specific tool name to get info for, or None for all tools
            
        Returns:
            Dictionary with tool information
        """
        if not self._initialized:
            return {}
        
        if tool_name:
            for tool in self.tools:
                if tool.name == tool_name:
                    return {
                        "name": tool.name,
                        "description": getattr(tool, 'description', 'No description available')
                    }
            return {}
        
        return {
            tool.name: {
                "description": getattr(tool, 'description', 'No description available')
            }
            for tool in self.tools
        }


# Convenience functions for common engineering patterns
async def quick_pipeline_design(requirements: str, model: str = "openai/o3") -> str:
    """
    Quick pipeline design function for one-off requirements.
    
    Args:
        requirements: The pipeline requirements
        model: Language model to use
        
    Returns:
        Pipeline design result
    """
    engineer = KeboolaPipelineEngineer(model=model)
    await engineer.initialize()
    return await engineer.design_pipeline(requirements)


# Example usage patterns
EXAMPLE_REQUESTS = [
    "Design a Customer 360 data pipeline",
    "Create an ETL pipeline for sales data",
    "Build a real-time analytics pipeline",
    "Design a data quality monitoring system",
    "Create a pipeline for customer segmentation",
    "Build a data warehouse loading pipeline",
    "Design a streaming data processing pipeline",
    "Create a pipeline for product recommendations",
    "Build a data lake ingestion pipeline",
    "Design a pipeline for financial reporting",
    "Create a pipeline for inventory management",
    "Build a pipeline for marketing attribution",
    "Design a pipeline for fraud detection",
    "Create a pipeline for A/B testing data",
    "Build a pipeline for user behavior analytics"
]


async def main():
    """
    Interactive demonstration of the generalized pipeline engineer agent.
    """
    print("🚀 Keboola Pipeline Engineer Agent")
    print("=" * 50)
    
    # Check environment variables
    required_env_vars = ["KBC_STORAGE_API_URL", "KBC_STORAGE_TOKEN", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables and try again.")
        return
    
    # Initialize the engineer
    engineer = KeboolaPipelineEngineer()
    
    try:
        await engineer.initialize()
        
        print(f"\n✅ Agent ready with {len(engineer.tools)} available tools")
        print("\n📋 Example pipeline requests you can make:")
        for i, example in enumerate(EXAMPLE_REQUESTS[:5], 1):
            print(f"  {i}. {example}")
        print("  ... and many more!")
        
        # Interactive loop
        print("\n" + "=" * 50)
        print("🔧 Describe your pipeline engineering needs!")
        print("   (Type 'quit' to exit)")
        print("=" * 50)
        
        while True:
            try:
                request = input("\n🏗️  Your pipeline request: ").strip()
                
                if request.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using the Pipeline Engineer Agent!")
                    break
                
                if not request:
                    print("❌ Please enter a pipeline request.")
                    continue
                
                print(f"\n⏳ Designing pipeline: {request}")
                print("=" * 50)
                
                # Design the pipeline
                result = await engineer.design_pipeline(request)
                
                print(f"\n🏗️  Pipeline Design:")
                print("=" * 50)
                print(result)
                print("=" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Engineering interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error during pipeline design: {e}")
                print("Please try a different request.")
                
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        print("Please check your Keboola credentials and connection.")


if __name__ == "__main__":
    asyncio.run(main()) 