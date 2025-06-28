#!/usr/bin/env python3
"""
Tool Verification Script for LangChain Data Analyst Agent

This script tests that all tools (Keboola MCP and additional tools) 
are loading correctly and can be initialized.
"""

import sys
import os
from dotenv import load_dotenv


def test_keboola_tools():
    """Test loading of Keboola MCP tools."""
    print("🔧 Testing Keboola MCP Tools...")
    
    try:
        from keboola_mcp_tools import get_keboola_tools
        
        tools = get_keboola_tools()
        
        if tools:
            print(f"✅ Successfully loaded {len(tools)} Keboola MCP tools")
            
            # Show tool categories
            tool_names = [tool.mcp_tool_name for tool in tools if hasattr(tool, 'mcp_tool_name')]
            
            # Categorize tools
            categories = {
                'Components': [t for t in tool_names if any(x in t for x in ['component', 'retrieve_components'])],
                'Storage': [t for t in tool_names if any(x in t for x in ['bucket', 'table', 'storage'])],
                'Transformations': [t for t in tool_names if 'transformation' in t],
                'Jobs': [t for t in tool_names if 'job' in t],
                'SQL': [t for t in tool_names if 'sql' in t or 'query' in t],
                'Documentation': [t for t in tool_names if 'docs' in t],
                'Other': [t for t in tool_names if not any(cat in t for cat in ['component', 'bucket', 'table', 'transformation', 'job', 'sql', 'query', 'docs'])]
            }
            
            print("\n📊 Tool Categories:")
            for category, category_tools in categories.items():
                if category_tools:
                    print(f"   • {category}: {len(category_tools)} tools")
                    for tool in category_tools[:3]:  # Show first 3 in each category
                        print(f"     - {tool}")
                    if len(category_tools) > 3:
                        print(f"     - ... and {len(category_tools) - 3} more")
            
            return True
        else:
            print("❌ No Keboola MCP tools loaded")
            return False
            
    except Exception as e:
        print(f"❌ Error loading Keboola MCP tools: {e}")
        return False


def test_additional_tools():
    """Test loading of additional tools."""
    print("\n🛠️ Testing Additional Tools...")
    
    try:
        from additional_tools import get_additional_tools
        
        tools = get_additional_tools()
        
        if tools:
            print(f"✅ Successfully loaded {len(tools)} additional tools")
            
            print("\n📋 Additional Tools:")
            for tool in tools:
                name = tool.name if hasattr(tool, 'name') else str(tool)
                desc = tool.description if hasattr(tool, 'description') else "No description"
                print(f"   • {name}: {desc[:60]}{'...' if len(desc) > 60 else ''}")
            
            return True
        else:
            print("❌ No additional tools loaded")
            return False
            
    except Exception as e:
        print(f"❌ Error loading additional tools: {e}")
        return False


def test_agent_initialization():
    """Test agent initialization."""
    print("\n🤖 Testing Agent Initialization...")
    
    try:
        from data_analyst_agent import DataAnalystAgent
        
        # Initialize with minimal verbosity
        agent = DataAnalystAgent(verbose=False)
        
        total_tools = len(agent.tools)
        print(f"✅ Agent initialized successfully with {total_tools} total tools")
        
        # Test tool info method
        tool_info = agent.get_tool_info()
        if tool_info:
            print("✅ Tool info retrieval working")
        else:
            print("⚠️ Tool info retrieval returned empty")
        
        # Test memory
        memory_summary = agent.get_memory_summary()
        print(f"✅ Memory system working: {memory_summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return False


def test_environment():
    """Test environment setup."""
    print("🌍 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv("../.env")
    
    # Check required environment variables
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API access',
        'KBC_STORAGE_API_URL': 'Keboola Storage API URL',
        'KBC_STORAGE_TOKEN': 'Keboola Storage Token'
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show partial value for security
            if 'KEY' in var or 'TOKEN' in var:
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file for full functionality")
        return False
    else:
        print("✅ All required environment variables are set")
        return True


def run_comprehensive_test():
    """Run comprehensive tool testing."""
    print("🧪 COMPREHENSIVE TOOL TESTING")
    print("=" * 50)
    
    # Test results
    results = {
        'Environment': test_environment(),
        'Keboola MCP Tools': test_keboola_tools(),
        'Additional Tools': test_additional_tools(),
        'Agent Initialization': test_agent_initialization()
    }
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1


def quick_tool_count():
    """Quick tool count test."""
    print("🔢 QUICK TOOL COUNT TEST")
    print("=" * 30)
    
    try:
        from keboola_mcp_tools import get_keboola_tools
        from additional_tools import get_additional_tools
        
        keboola_tools = get_keboola_tools()
        additional_tools = get_additional_tools()
        
        print(f"Keboola MCP Tools: {len(keboola_tools)}")
        print(f"Additional Tools: {len(additional_tools)}")
        print(f"Total Tools: {len(keboola_tools) + len(additional_tools)}")
        
        if len(keboola_tools) >= 30:  # Expecting ~31 Keboola tools
            print("✅ Expected number of Keboola tools loaded")
        else:
            print("⚠️ Fewer Keboola tools than expected")
        
        if len(additional_tools) >= 5:  # Expecting ~7 additional tools
            print("✅ Expected number of additional tools loaded")
        else:
            print("⚠️ Fewer additional tools than expected")
            
        return 0
        
    except Exception as e:
        print(f"❌ Error in tool count test: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        sys.exit(quick_tool_count())
    else:
        sys.exit(run_comprehensive_test()) 