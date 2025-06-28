#!/usr/bin/env python3
"""
DSPy + Keboola MCP Demo

Main entry point for the Keboola MCP + DSPy agent demonstration.
This script provides an interactive interface to test AI agents 
with your Keboola data platform.
"""

import asyncio
import os
import sys

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import KeboolaDataAnalyst, KeboolaPipelineEngineer


async def main_demo():
    """Main interactive demo for DSPy + Keboola MCP agents."""
    
    print("🚀 DSPy + Keboola MCP Agent Demo")
    print("=" * 50)
    
    # Check environment variables
    required_env_vars = ["KBC_STORAGE_API_URL", "KBC_STORAGE_TOKEN", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file and try again.")
        print("See README.md for setup instructions.")
        return
    
    print("✅ Environment configured")
    
    # Initialize agents
    print("\n🔧 Initializing AI agents...")
    
    try:
        analyst = KeboolaDataAnalyst()
        engineer = KeboolaPipelineEngineer()
        
        print("   Initializing Data Analyst...")
        await analyst.initialize()
        print(f"   ✅ Data Analyst ready with {len(analyst.tools)} tools")
        
        print("   Initializing Pipeline Engineer...")
        await engineer.initialize()
        print(f"   ✅ Pipeline Engineer ready with {len(engineer.tools)} tools")
        
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        print("Please check your Keboola credentials and try again.")
        return
    
    print("\n🎉 All agents ready!")
    print("=" * 50)
    
    # Interactive loop
    while True:
        print("\n📋 Choose an AI Agent:")
        print("1. 📊 Data Analyst - Explore and analyze your data")
        print("2. 🔧 Pipeline Engineer - Design data pipelines")
        print("3. 🚪 Exit")
        
        try:
            choice = input("\nSelect (1-3): ").strip()
            
            if choice == "3":
                print("\n👋 Thanks for using the demo!")
                break
            
            if choice == "1":
                agent = analyst
                agent_name = "Data Analyst"
                examples = [
                    "What data is available in my Keboola project?",
                    "Analyze my customer data and find insights",
                    "Show me data quality issues across all tables"
                ]
            elif choice == "2":
                agent = engineer
                agent_name = "Pipeline Engineer"
                examples = [
                    "Design a Customer 360 data pipeline",
                    "Create an ETL pipeline for sales analytics",
                    "Build a data quality monitoring pipeline"
                ]
            else:
                print("❌ Invalid choice. Please select 1, 2, or 3.")
                continue
            
            print(f"\n🤖 {agent_name} Selected")
            print("-" * 30)
            print("Example questions:")
            for example in examples:
                print(f"  • {example}")
            
            query = input(f"\n💬 Ask the {agent_name}: ").strip()
            
            if not query:
                print("❌ Please enter a question.")
                continue
            
            print(f"\n⏳ {agent_name} is working on your request...")
            print("=" * 50)
            
            # Execute the query
            if choice == "1":
                result = await agent.analyze_data(query)
            elif choice == "2":
                result = await agent.design_pipeline(query)
            
            print(f"\n✅ {agent_name} Response:")
            print("=" * 50)
            print(result)
            print("=" * 50)
            
            # Ask if user wants to continue
            continue_choice = input("\nAsk another question? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("\n👋 Thanks for using the demo!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try a different question.")


if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv(".env")  # Load from current directory
    except ImportError:
        print("⚠️  python-dotenv not installed. Set environment variables manually.")
    
    # Run the demo
    asyncio.run(main_demo()) 