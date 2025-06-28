#!/usr/bin/env python3
"""
Test Tools: Verify Keboola MCP Tools Loading

This script verifies that all expected Keboola MCP tools are loading correctly
and displays detailed information about available tools.
"""

import asyncio
import os
import sys

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import KeboolaDataAnalyst, KeboolaPipelineEngineer


async def test_tools():
    """Test that all tools are loading correctly for each agent."""
    
    print("🔧 Testing Keboola MCP Tool Loading")
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
    
    print("✅ Environment variables configured")
    
    # Test each agent
    agents = [
        ("📊 Data Analyst", KeboolaDataAnalyst()),
        ("🔧 Pipeline Engineer", KeboolaPipelineEngineer())
    ]
    
    all_tools_loaded = True
    
    for agent_name, agent_instance in agents:
        print(f"\n🧪 Testing {agent_name}")
        print("-" * 30)
        
        try:
            # Initialize the agent
            await agent_instance.initialize()
            
            # Get tool information
            tool_count = len(agent_instance.tools)
            tool_names = agent_instance.get_available_tools()
            
            print(f"✅ {agent_name} initialized successfully")
            print(f"📊 Loaded {tool_count} tools")
            
            # Expected tool categories and approximate counts
            expected_categories = {
                "Storage": ["retrieve_buckets", "get_bucket_detail", "retrieve_bucket_tables", "get_table_detail", "query_table", "update_bucket_description", "update_table_description"],
                "Components": ["retrieve_components_configurations", "get_component_configuration", "retrieve_transformations", "create_sql_transformation", "update_sql_transformation_configuration", "get_component", "create_component_root_configuration", "create_component_row_configuration", "update_component_root_configuration", "update_component_row_configuration", "get_component_configuration_examples", "find_component_id"],
                "Jobs": ["retrieve_jobs", "get_job_detail", "start_job"],
                "Flows": ["create_flow", "retrieve_flows", "update_flow", "get_flow_detail", "get_flow_schema"],
                "SQL": ["get_sql_dialect", "query_table"],
                "Documentation": ["docs_query"],
                "Project": ["get_project_info"]
            }
            
            # Check tool categories
            print("\n📋 Tool Categories:")
            for category, expected_tools in expected_categories.items():
                found_tools = [tool for tool in tool_names if any(expected in tool for expected in expected_tools)]
                print(f"   {category}: {len(found_tools)} tools")
                
                # Show some example tools for verification
                if found_tools:
                    example_tools = found_tools[:3]  # Show first 3 as examples
                    print(f"      Examples: {', '.join(example_tools)}")
            
            # Verify minimum expected tool count
            if tool_count < 25:  # We expect at least 25+ tools
                print(f"⚠️  Warning: Only {tool_count} tools loaded, expected 25+")
                all_tools_loaded = False
            else:
                print(f"✅ Tool count looks good: {tool_count} tools")
            
            # Display all available tools for verification
            print(f"\n📝 All Available Tools ({tool_count}):")
            for i, tool_name in enumerate(sorted(tool_names), 1):
                print(f"   {i:2d}. {tool_name}")
            
        except Exception as e:
            print(f"❌ Failed to initialize {agent_name}: {e}")
            all_tools_loaded = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_tools_loaded:
        print("🎉 SUCCESS: All agents initialized with expected tools!")
        print("✅ Keboola MCP Server integration is working correctly")
    else:
        print("❌ ISSUES DETECTED: Some tools may not be loading correctly")
        print("🔍 Please check your Keboola credentials and server version")
    
    print("=" * 50)


async def main():
    """Main test function."""
    await test_tools()


if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv("../.env")  # Load from parent directory
    except ImportError:
        print("⚠️  python-dotenv not installed. Make sure to set environment variables manually.")
    
    # Run the test
    asyncio.run(main()) 