"""
LangChain Data Analyst Agent with Keboola MCP Integration

This module implements a powerful data analyst agent using LangChain that integrates
with Keboola MCP Server for data platform operations and includes additional tools
for comprehensive data analysis capabilities.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler

from keboola_mcp_tools import get_keboola_tools
from additional_tools import get_additional_tools


class DataAnalystAgent:
    """
    A comprehensive data analyst agent that combines Keboola MCP tools with additional
    analysis capabilities using LangChain's agent framework.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.1,
        max_tokens: int = 4000,
        verbose: bool = True,
        memory_window: int = 10
    ):
        """
        Initialize the Data Analyst Agent.
        
        Args:
            model: OpenAI model to use
            temperature: Model temperature for creativity vs consistency
            max_tokens: Maximum tokens for model response
            verbose: Whether to show detailed agent reasoning
            memory_window: Number of conversation turns to remember
        """
        # Load environment variables
        load_dotenv("../.env")
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose
        
        # Initialize LLM with streaming for better user experience
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()] if verbose else []
        )
        
        # Initialize memory for conversation context
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=memory_window,
            return_messages=True
        )
        
        # Load tools
        self.tools = self._load_all_tools()
        
        # Initialize agent
        self.agent = self._create_agent()
        
        print(f"✅ Data Analyst Agent initialized with {len(self.tools)} tools")
        self._print_available_tools()
    
    def _load_all_tools(self) -> List:
        """Load all available tools for the agent."""
        tools = []
        
        # Load Keboola MCP tools
        try:
            keboola_tools = get_keboola_tools()
            tools.extend(keboola_tools)
            print(f"✅ Loaded {len(keboola_tools)} Keboola MCP tools")
        except Exception as e:
            print(f"⚠️ Failed to load Keboola MCP tools: {e}")
        
        # Load additional tools
        try:
            additional_tools = get_additional_tools()
            tools.extend(additional_tools)
            print(f"✅ Loaded {len(additional_tools)} additional tools")
        except Exception as e:
            print(f"⚠️ Failed to load additional tools: {e}")
        
        return tools
    
    def _create_agent(self):
        """Create the LangChain agent with all tools."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=self.verbose,
            max_iterations=10,
            early_stopping_method="generate",
            handle_parsing_errors=True,
            agent_kwargs={
                "system_message": self._get_system_prompt()
            }
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """You are a highly skilled Data Analyst Agent with access to comprehensive data analysis tools.

Your capabilities include:

KEBOOLA DATA PLATFORM:
- Access to Keboola's data storage, transformations, and pipeline management
- Query and analyze data stored in Keboola buckets and tables
- Create and manage data transformations
- Monitor data pipeline jobs and workflows
- Retrieve component configurations and metadata

ADDITIONAL ANALYSIS TOOLS:
- Web search for research and context gathering
- Financial data analysis using real-time market data
- Data visualization and charting capabilities
- Statistical analysis and correlation studies
- Web scraping for external data collection
- Python code execution for custom analysis
- Wikipedia research for background information

APPROACH:
1. Always start by understanding the user's specific analytical needs
2. Use Keboola tools to access and explore available data
3. Apply appropriate analysis techniques based on the data and question
4. Create visualizations when helpful for understanding
5. Provide clear, actionable insights with supporting evidence
6. Suggest next steps or follow-up analyses when relevant

BEST PRACTICES:
- Ask clarifying questions if the request is ambiguous
- Explain your analytical approach and reasoning
- Use multiple tools when necessary for comprehensive analysis
- Present findings in a clear, structured format
- Always validate data quality and note any limitations

You are helpful, thorough, and focused on delivering valuable data insights."""
    
    def _print_available_tools(self):
        """Print summary of available tools."""
        keboola_tools = [t for t in self.tools if hasattr(t, 'name') and t.name.startswith('keboola_')]
        other_tools = [t for t in self.tools if not (hasattr(t, 'name') and t.name.startswith('keboola_'))]
        
        print(f"\n📊 AVAILABLE TOOLS:")
        print(f"   • Keboola MCP Tools: {len(keboola_tools)}")
        print(f"   • Additional Tools: {len(other_tools)}")
        
        if keboola_tools:
            print(f"\n🔧 Keboola Tools:")
            for tool in keboola_tools[:5]:  # Show first 5
                name = tool.name.replace('keboola_', '') if hasattr(tool, 'name') else str(tool)
                print(f"   • {name}")
            if len(keboola_tools) > 5:
                print(f"   • ... and {len(keboola_tools) - 5} more")
        
        if other_tools:
            print(f"\n🛠️ Additional Tools:")
            for tool in other_tools:
                name = tool.name if hasattr(tool, 'name') else str(tool)
                print(f"   • {name}")
        print()
    
    def analyze(self, query: str) -> str:
        """
        Perform data analysis based on the user's query.
        
        Args:
            query: The analysis request or question
            
        Returns:
            Analysis results and insights
        """
        try:
            print(f"\n🔍 ANALYZING: {query}\n")
            print("=" * 60)
            
            # Run the agent
            result = self.agent.invoke({"input": query})
            
            # Extract the output from the result
            if isinstance(result, dict) and 'output' in result:
                result = result['output']
            
            print("\n" + "=" * 60)
            print("✅ ANALYSIS COMPLETE")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_tool_info(self, tool_name: str = None) -> str:
        """
        Get information about available tools.
        
        Args:
            tool_name: Specific tool name to get info about, or None for all tools
            
        Returns:
            Tool information
        """
        if tool_name:
            # Find specific tool
            for tool in self.tools:
                if hasattr(tool, 'name') and tool.name == tool_name:
                    return f"Tool: {tool.name}\nDescription: {tool.description}"
            return f"Tool '{tool_name}' not found"
        else:
            # List all tools
            tool_list = []
            for tool in self.tools:
                name = tool.name if hasattr(tool, 'name') else str(tool)
                desc = tool.description if hasattr(tool, 'description') else "No description"
                tool_list.append(f"• {name}: {desc}")
            
            return f"Available Tools ({len(self.tools)}):\n" + "\n".join(tool_list)
    
    def clear_memory(self):
        """Clear the agent's conversation memory."""
        self.memory.clear()
        print("🧠 Memory cleared")
    
    def get_memory_summary(self) -> str:
        """Get a summary of the current conversation memory."""
        if hasattr(self.memory, 'chat_memory') and self.memory.chat_memory.messages:
            return f"Memory contains {len(self.memory.chat_memory.messages)} messages"
        return "Memory is empty"


def main():
    """Example usage of the Data Analyst Agent."""
    
    # Initialize the agent
    agent = DataAnalystAgent(verbose=True)
    
    # Example analyses
    examples = [
        "What data is available in my Keboola project? Please provide an overview of buckets and tables.",
        "Show me the current stock price and performance metrics for Apple (AAPL).",
        "Search for recent news about artificial intelligence trends in data analytics.",
        "Can you help me understand what transformations are configured in my Keboola project?"
    ]
    
    print("🚀 DATA ANALYST AGENT DEMO")
    print("=" * 50)
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("1. Enter your own analysis query")
        print("2. Run example analyses")
        print("3. Show available tools")
        print("4. Clear memory")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            query = input("\nEnter your analysis query: ").strip()
            if query:
                result = agent.analyze(query)
                print(f"\n📊 RESULT:\n{result}")
            
        elif choice == "2":
            print("\n📋 EXAMPLE ANALYSES:")
            for i, example in enumerate(examples, 1):
                print(f"{i}. {example}")
            
            try:
                example_choice = int(input("\nSelect example (1-4): ")) - 1
                if 0 <= example_choice < len(examples):
                    result = agent.analyze(examples[example_choice])
                    print(f"\n📊 RESULT:\n{result}")
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number")
                
        elif choice == "3":
            print(f"\n{agent.get_tool_info()}")
            
        elif choice == "4":
            agent.clear_memory()
            
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main() 