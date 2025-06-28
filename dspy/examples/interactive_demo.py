#!/usr/bin/env python3
"""
Interactive Demo: Keboola MCP + DSPy Agents

This script allows you to interactively test the DSPy agents with your own queries.
Simply run the script and enter your data analysis questions when prompted.
"""

import asyncio
import os
import sys

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import KeboolaDataAnalyst, KeboolaPipelineEngineer


async def interactive_demo():
    """Interactive demo that lets users enter their own queries."""
    
    print("🚀 Welcome to the Interactive Keboola MCP + DSPy Demo!")
    print("=" * 60)
    
    # Check environment variables
    required_env_vars = ["KBC_STORAGE_API_URL", "KBC_STORAGE_TOKEN", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables in your .env file and try again.")
        return
    
    print("✅ Environment variables configured")
    
    # Initialize agents
    print("\n🔧 Initializing agents...")
    
    agents = {
        "analyst": ("📊 Data Analyst", KeboolaDataAnalyst()),
        "engineer": ("🔧 Pipeline Engineer", KeboolaPipelineEngineer())
    }
    
    # Initialize all agents
    for agent_key, (agent_name, agent_instance) in agents.items():
        try:
            print(f"   Initializing {agent_name}...")
            await agent_instance.initialize()
            print(f"   ✅ {agent_name} ready with {len(agent_instance.tools)} tools")
        except Exception as e:
            print(f"   ❌ Failed to initialize {agent_name}: {e}")
            return
    
    print(f"\n🎉 All agents initialized successfully!")
    print("=" * 60)
    
    # Interactive loop
    while True:
        print("\n📋 Available Agents:")
        print("1. 📊 Data Analyst - Explore data, perform analysis, generate insights")
        print("2. 🔧 Pipeline Engineer - Design ETL pipelines, data architecture")
        print("3. 🚪 Exit")
        
        try:
            choice = input("\nSelect an agent (1-3): ").strip()
            
            if choice == "3":
                print("\n👋 Thanks for using the Keboola MCP + DSPy Demo!")
                break
            
            if choice not in ["1", "2"]:
                print("❌ Invalid choice. Please select 1, 2, or 3.")
                continue
            
            # Map choice to agent
            agent_map = {
                "1": ("analyst", "📊 Data Analyst"),
                "2": ("engineer", "🔧 Pipeline Engineer")
            }
            
            agent_key, agent_display_name = agent_map[choice]
            _, agent_instance = agents[agent_key]
            
            print(f"\n🤖 You selected: {agent_display_name}")
            print("=" * 40)
            
            # Get user query
            print("\n💬 Enter your query (or 'back' to return to agent selection):")
            print("Examples:")
            if agent_key == "analyst":
                print("  - 'What data do I have available in my project?'")
                print("  - 'Analyze my customer data and find key insights'")
                print("  - 'Show me revenue trends and top performing products'")
            elif agent_key == "engineer":
                print("  - 'Design a Customer 360 data pipeline'")
                print("  - 'Create an ETL pipeline for sales data'")
                print("  - 'Build a real-time analytics pipeline'")
            
            query = input("\n🔍 Your query: ").strip()
            
            if query.lower() == 'back':
                continue
            
            if not query:
                print("❌ Please enter a query.")
                continue
            
            print(f"\n⏳ Processing your query with {agent_display_name}...")
            print("=" * 40)
            
            # Execute the query based on agent type
            try:
                if agent_key == "analyst":
                    result = await agent_instance.analyze_data(query)
                elif agent_key == "engineer":
                    result = await agent_instance.design_pipeline(query)
                
                print(f"\n✅ {agent_display_name} Response:")
                print("=" * 40)
                print(result)
                
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
                print("Please try a different query or check your environment setup.")
            
            # Ask if user wants to continue
            print("\n" + "=" * 60)
            continue_choice = input("Would you like to ask another question? (y/n): ").strip().lower()
            
            if continue_choice not in ['y', 'yes']:
                print("\n👋 Thanks for using the Keboola MCP + DSPy Demo!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again or check your setup.")


if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv("../.env")  # Load from parent directory
    except ImportError:
        print("⚠️  python-dotenv not installed. Make sure to set environment variables manually.")
    
    # Run the interactive demo
    asyncio.run(interactive_demo()) 