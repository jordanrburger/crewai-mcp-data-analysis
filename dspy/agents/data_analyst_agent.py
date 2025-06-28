"""
DSPy Data Analyst Agent for Keboola MCP Server

A generalized, modular data analyst agent that can handle any type of data analysis
request dynamically using the Keboola MCP Server tools.
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import dspy


class DataAnalysisSignature(dspy.Signature):
    """
    You are an expert data analyst with access to a comprehensive set of Keboola data platform tools.
    You can explore data, run SQL queries, manage transformations, and analyze any type of data.
    
    Your approach should be:
    1. Understand the user's request thoroughly
    2. Explore available data sources when needed
    3. Use appropriate tools to gather and analyze data
    4. Apply statistical and analytical thinking
    5. Provide clear, actionable insights
    6. Suggest next steps or recommendations
    
    Always be thorough but efficient in your analysis approach.
    """
    
    user_request: str = dspy.InputField(
        desc="The user's data analysis request, question, or business problem"
    )
    
    analysis_result: str = dspy.OutputField(
        desc="Comprehensive analysis results with findings, insights, and recommendations"
    )


class KeboolaDataAnalyst:
    """
    A modular, generalized data analyst agent that can handle any data analysis task
    using Keboola MCP Server tools dynamically.
    """
    
    def __init__(self, model: str = "openai/o3"):
        """
        Initialize the data analyst agent.
        
        Args:
            model: The language model to use for analysis
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
                print(f"✅ Initialized Keboola Data Analyst with {len(self.tools)} tools")
    
    async def analyze_data(self, request: str) -> str:
        """
        Perform data analysis based on any user request.
        
        This is the main method that handles all types of data analysis requests
        dynamically using the available Keboola tools.
        
        Args:
            request: The user's analysis request or business question
            
        Returns:
            Analysis results with insights and recommendations
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
                agent = dspy.ReAct(DataAnalysisSignature, tools=session_tools)
                
                # Execute the analysis
                result = await agent.acall(user_request=request)
                return result.analysis_result
    
    def get_available_tools(self) -> List[str]:
        """
        Get a list of available tool names for reference.
        
        Returns:
            List of tool names that can be used for analysis
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


# Convenience functions for common analysis patterns
async def quick_analysis(question: str, model: str = "openai/o3") -> str:
    """
    Quick analysis function for one-off questions.
    
    Args:
        question: The analysis question
        model: Language model to use
        
    Returns:
        Analysis result
    """
    analyst = KeboolaDataAnalyst(model=model)
    await analyst.initialize()
    return await analyst.analyze_data(question)


# Example usage patterns
EXAMPLE_REQUESTS = [
    "What data is available in my Keboola project?",
    "Analyze customer behavior patterns in my data",
    "Find data quality issues across all tables",
    "Show me revenue trends over the last 12 months",
    "Create a customer segmentation analysis",
    "Identify the most valuable customers",
    "What are the top-performing products?",
    "Analyze website traffic patterns",
    "Find correlations between different data sources",
    "Generate a data quality report",
    "Show me incomplete or missing data",
    "Analyze seasonal trends in the business",
    "Create a cohort analysis of customers",
    "Find anomalies in the data",
    "Analyze conversion funnel performance"
]


async def main():
    """
    Interactive demonstration of the generalized data analyst agent.
    """
    print("🚀 Keboola Data Analyst Agent")
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
    
    # Initialize the analyst
    analyst = KeboolaDataAnalyst()
    
    try:
        await analyst.initialize()
        
        print(f"\n✅ Agent ready with {len(analyst.tools)} available tools")
        print("\n📋 Example questions you can ask:")
        for i, example in enumerate(EXAMPLE_REQUESTS[:5], 1):
            print(f"  {i}. {example}")
        print("  ... and many more!")
        
        # Interactive loop
        print("\n" + "=" * 50)
        print("💬 Ask me anything about your data!")
        print("   (Type 'quit' to exit)")
        print("=" * 50)
        
        while True:
            try:
                question = input("\n🔍 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using the Data Analyst Agent!")
                    break
                
                if not question:
                    print("❌ Please enter a question.")
                    continue
                
                print(f"\n⏳ Analyzing: {question}")
                print("=" * 50)
                
                # Perform the analysis
                result = await analyst.analyze_data(question)
                
                print(f"\n📊 Analysis Results:")
                print("=" * 50)
                print(result)
                print("=" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Analysis interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error during analysis: {e}")
                print("Please try a different question.")
                
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        print("Please check your Keboola credentials and connection.")


if __name__ == "__main__":
    asyncio.run(main()) 