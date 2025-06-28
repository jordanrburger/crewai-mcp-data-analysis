"""
CrewAI Data Analysis Crew with Keboola MCP Server Integration

This script demonstrates how to create a CrewAI crew that uses the Keboola MCP Server
for advanced data analysis operations. The crew consists of specialized agents that
can interact with your Keboola project through the MCP protocol.

Requirements:
- Keboola project with proper API token and workspace schema
- Environment variables set for Keboola authentication
- CrewAI MCP Toolbox installed
"""

import asyncio
import os
from typing import List, Optional
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai_mcp_toolbox import MCPToolSet

# Load environment variables
load_dotenv()

class KeboolaDataAnalysisCrew:
    """
    A CrewAI crew specialized in data analysis using Keboola's MCP Server.
    This crew can explore data, perform analysis, and create data transformations.
    """
    
    def __init__(self):
        self.validate_environment()
        self.mcp_toolset = self.setup_mcp_toolset()
        self.agents = {}
        self.tasks = []
    
    def validate_environment(self):
        """Validate that all required environment variables are set."""
        required_vars = [
            'OPENAI_API_KEY',
            'KBC_STORAGE_TOKEN', 
            'KBC_WORKSPACE_SCHEMA',
            'KBC_STORAGE_API_URL'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print("⚠️  Missing required environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\nPlease set these in your .env file")
            raise ValueError(f"Missing environment variables: {missing_vars}")
        
        print("✅ All required environment variables are set")
    
    def setup_mcp_toolset(self):
        """Initialize the MCP toolset with Keboola server configuration."""
        try:
            print("🔧 Setting up Keboola MCP Server connection...")
            
            # Get environment variables
            api_url = os.getenv('KBC_STORAGE_API_URL')
            storage_token = os.getenv('KBC_STORAGE_TOKEN')
            workspace_schema = os.getenv('KBC_WORKSPACE_SCHEMA')
            
            # Create environment for the MCP server subprocess
            env = os.environ.copy()
            env.update({
                'KBC_STORAGE_API_URL': api_url,
                'KBC_STORAGE_TOKEN': storage_token,
                'KBC_WORKSPACE_SCHEMA': workspace_schema
            })
            
            # Create the MCP toolset with proper environment variables
            toolset = MCPToolSet(
                command='uvx',
                args=[
                    'keboola_mcp_server',
                    '--transport', 'stdio',
                    '--log-level', 'INFO',
                    '--api-url', api_url
                ],
                env=env
            )
            
            print("✅ MCP toolset configured successfully")
            return toolset
            
        except Exception as e:
            print(f"❌ Failed to setup MCP toolset: {e}")
            raise
    
    def initialize_mcp(self):
        """Initialize the MCP connection and discover tools."""
        try:
            print("🚀 Initializing MCP connection...")
            self.mcp_toolset.initialize()
            
            print(f"📋 Discovered {len(self.mcp_toolset.tools)} Keboola tools:")
            for i, tool in enumerate(self.mcp_toolset.tools[:10], 1):
                name = getattr(tool, 'name', 'Unknown')
                desc = getattr(tool, 'description', 'No description')
                print(f"   {i}. {name}: {desc[:60]}...")
            
            if len(self.mcp_toolset.tools) > 10:
                print(f"   ... and {len(self.mcp_toolset.tools) - 10} more tools")
                
        except Exception as e:
            print(f"❌ Failed to initialize MCP: {e}")
            raise
    
    def create_agents(self):
        """Create specialized data analysis agents with Keboola tools."""
        
        self.agents['data_explorer'] = Agent(
            role='Data Explorer',
            goal='Discover and explore data structures, schemas, and relationships in Keboola',
            backstory="""You are an expert data explorer who understands data architectures and 
            can quickly identify key datasets, their relationships, and data quality issues. 
            You use Keboola's tools to navigate through buckets, tables, and understand data lineage.""",
            tools=self.mcp_toolset.tools,
            verbose=True,
            allow_delegation=False
        )
        
        self.agents['data_analyst'] = Agent(
            role='Data Analyst', 
            goal='Perform advanced data analysis and generate insights using SQL queries',
            backstory="""You are a skilled data analyst who can write complex SQL queries, 
            perform statistical analysis, and identify trends and patterns in data. 
            You use Keboola's query capabilities to extract meaningful insights.""",
            tools=self.mcp_toolset.tools,
            verbose=True,
            allow_delegation=False
        )
        
        self.agents['pipeline_engineer'] = Agent(
            role='Pipeline Engineer',
            goal='Create and optimize data transformations and workflows',
            backstory="""You are an expert in data engineering who can design efficient 
            data transformations, create SQL transformations, and optimize data pipelines. 
            You understand best practices for data processing in Keboola.""",
            tools=self.mcp_toolset.tools,
            verbose=True,
            allow_delegation=False
        )
    
    def create_tasks(self, objective: str):
        """Create tasks based on the analysis objective."""
        
        self.tasks = [
            Task(
                description=f"""
                Explore the Keboola project to understand the data landscape:
                1. List all available buckets and their purposes
                2. Identify key tables and their schemas
                3. Understand data relationships and dependencies
                4. Assess data freshness and quality
                
                Analysis objective: {objective}
                
                Provide a comprehensive overview of the data ecosystem.
                """,
                agent=self.agents['data_explorer'],
                expected_output="Detailed report on data structure, quality, and relationships"
            ),
            
            Task(
                description=f"""
                Based on the data exploration, perform detailed analysis:
                1. Query relevant datasets to understand data distributions
                2. Identify key metrics and KPIs
                3. Look for trends, patterns, and anomalies
                4. Generate statistical summaries
                
                Analysis objective: {objective}
                
                Focus on actionable insights that address the objective.
                """,
                agent=self.agents['data_analyst'],
                expected_output="Data analysis report with insights, trends, and recommendations"
            ),
            
            Task(
                description=f"""
                Create optimized data transformations and recommendations:
                1. Design SQL transformations to support the analysis
                2. Suggest data pipeline improvements
                3. Recommend data quality enhancements
                4. Propose automation opportunities
                
                Analysis objective: {objective}
                
                Provide practical implementation recommendations.
                """,
                agent=self.agents['pipeline_engineer'],
                expected_output="Technical recommendations for data transformations and pipeline optimizations"
            )
        ]
    
    def run_analysis(self, objective: str = "Comprehensive data analysis and insights generation"):
        """Run the complete data analysis workflow."""
        try:
            # Initialize MCP connection
            self.initialize_mcp()
            
            # Create agents and tasks
            self.create_agents()
            self.create_tasks(objective)
            
            # Create and run the crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True
            )
            
            print(f"\n🎯 Starting analysis: {objective}")
            print("=" * 80)
            
            result = crew.kickoff()
            
            print("\n✅ Analysis completed successfully!")
            print("=" * 80)
            
            return result
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            raise
        finally:
            # Cleanup MCP connection
            if hasattr(self, 'mcp_toolset') and self.mcp_toolset is not None:
                try:
                    self.mcp_toolset.cleanup()
                except Exception as cleanup_error:
                    print(f"⚠️  Warning: Failed to cleanup MCP connection: {cleanup_error}")

def main():
    """Main function to demonstrate the Keboola Data Analysis Crew."""
    print("🤖 Keboola Data Analysis Crew with MCP Integration")
    print("=" * 60)
    
    try:
        # Check if .env file exists
        if not os.path.exists('.env'):
            print("⚠️  No .env file found. Please create one based on env_template.txt")
            print("Required variables:")
            print("- OPENAI_API_KEY")
            print("- KBC_STORAGE_TOKEN") 
            print("- KBC_WORKSPACE_SCHEMA")
            print("- KBC_STORAGE_API_URL")
            return
        
        # Create and run the analysis crew
        crew = KeboolaDataAnalysisCrew()
        
        result = crew.run_analysis(
            objective="Analyze our data ecosystem to identify key business metrics, data quality issues, and optimization opportunities"
        )
        
        print(f"\n📊 Final Result:\n{result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 