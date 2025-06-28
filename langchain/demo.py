#!/usr/bin/env python3
"""
LangChain Data Analyst Agent Demo

A simple demonstration of the LangChain-based data analyst agent
with Keboola MCP integration and additional analysis tools.
"""

import sys
import os
from data_analyst_agent import DataAnalystAgent


def run_demo():
    """Run the data analyst agent demo."""
    
    print("🚀 LANGCHAIN DATA ANALYST AGENT DEMO")
    print("=" * 60)
    print("This demo showcases a powerful data analyst agent built with LangChain")
    print("that integrates with Keboola MCP Server and additional analysis tools.")
    print("=" * 60)
    
    try:
        # Initialize the agent
        print("\n🔧 Initializing Data Analyst Agent...")
        agent = DataAnalystAgent(verbose=True)
        
        # Demo scenarios
        scenarios = [
            {
                "name": "Keboola Project Overview",
                "query": "What data is available in my Keboola project? Please provide an overview of buckets and tables.",
                "description": "Explore available data in Keboola project"
            },
            {
                "name": "Financial Analysis",
                "query": "Get the current stock price and key metrics for Tesla (TSLA) and create a summary analysis.",
                "description": "Analyze financial data for a specific stock"
            },
            {
                "name": "Market Research",
                "query": "Search for recent news about 'data engineering trends 2024' and summarize the key findings.",
                "description": "Research current industry trends"
            },
            {
                "name": "Data Transformation Review",
                "query": "Show me what transformations are configured in my Keboola project and their purposes.",
                "description": "Review data transformation configurations"
            }
        ]
        
        # Interactive menu
        while True:
            print("\n📋 AVAILABLE DEMO SCENARIOS:")
            for i, scenario in enumerate(scenarios, 1):
                print(f"{i}. {scenario['name']}: {scenario['description']}")
            print("5. Custom Query")
            print("6. Show Available Tools")
            print("7. Exit")
            
            try:
                choice = input("\nSelect scenario (1-7): ").strip()
                
                if choice in ['1', '2', '3', '4']:
                    scenario_idx = int(choice) - 1
                    scenario = scenarios[scenario_idx]
                    
                    print(f"\n🎯 RUNNING SCENARIO: {scenario['name']}")
                    print(f"Query: {scenario['query']}")
                    print("-" * 50)
                    
                    result = agent.analyze(scenario['query'])
                    
                    print(f"\n✅ SCENARIO COMPLETE")
                    print("-" * 50)
                    
                elif choice == '5':
                    custom_query = input("\nEnter your custom analysis query: ").strip()
                    if custom_query:
                        print(f"\n🎯 RUNNING CUSTOM QUERY")
                        print(f"Query: {custom_query}")
                        print("-" * 50)
                        
                        result = agent.analyze(custom_query)
                        
                        print(f"\n✅ CUSTOM QUERY COMPLETE")
                        print("-" * 50)
                    else:
                        print("❌ Empty query provided")
                        
                elif choice == '6':
                    print("\n🛠️ AVAILABLE TOOLS:")
                    print(agent.get_tool_info())
                    
                elif choice == '7':
                    print("\n👋 Thank you for trying the LangChain Data Analyst Agent!")
                    break
                    
                else:
                    print("❌ Invalid choice. Please select 1-7.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nPlease ensure:")
        print("1. Environment variables are set (KBC_STORAGE_API_URL, KBC_STORAGE_TOKEN)")
        print("2. OpenAI API key is configured")
        print("3. All dependencies are installed")
        return 1
    
    return 0


def quick_test():
    """Run a quick test of the agent."""
    print("🧪 QUICK TEST MODE")
    print("=" * 30)
    
    try:
        agent = DataAnalystAgent(verbose=False)
        
        # Simple test query
        test_query = "What tools do you have available for data analysis?"
        print(f"\nTest Query: {test_query}")
        print("-" * 30)
        
        result = agent.analyze(test_query)
        print(f"\nResult: {result}")
        
        print("\n✅ Quick test completed successfully!")
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sys.exit(quick_test())
    else:
        sys.exit(run_demo()) 