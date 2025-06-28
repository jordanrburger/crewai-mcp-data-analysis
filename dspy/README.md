# DSPy + Keboola MCP Server Demo

This demo showcases how to use DSPy with the Keboola MCP Server to build AI-powered data analysis and data engineering agents. The Keboola MCP Server provides a comprehensive set of tools for data platform operations, making it an ideal source for AI agents to perform complex data tasks.

## Overview

The Keboola MCP Server exposes powerful data platform capabilities through the Model Context Protocol (MCP), enabling AI agents to:

- **Query and analyze data** from Keboola storage buckets and tables
- **Create and manage SQL transformations** with natural language
- **Build and orchestrate data pipelines** and flows
- **Monitor job execution** and debug data processing issues
- **Manage data documentation** and metadata

## What's Included

This demo includes two core DSPy agents that demonstrate different use cases:

## 📁 Project Structure

```
dspy/
├── agents/                    # AI Agent implementations
│   ├── data_analyst_agent.py  # Data exploration and analysis
│   └── pipeline_engineer_agent.py # Data pipeline design
├── examples/                  # Demo and test scripts
│   ├── interactive_demo.py    # Advanced interactive interface
│   └── test_tools.py         # Tool loading verification
├── demo.py                   # Main demo entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🤖 Available Agents

1. **📊 Data Analyst** (`agents/data_analyst_agent.py`) - Explores datasets, performs analysis, and generates insights
2. **🔧 Pipeline Engineer** (`agents/pipeline_engineer_agent.py`) - Designs and manages data pipelines

## Key Features Demonstrated

### 🔍 Data Exploration & Analysis
- Discover available datasets and their structure
- Perform exploratory data analysis with SQL queries
- Generate insights and recommendations from data
- Create visualizations and reports

### 🛠️ Data Engineering
- Build SQL transformations using natural language descriptions
- Create and manage data processing flows
- Monitor job execution and handle errors
- Optimize data pipelines for performance

### 📊 Data Quality & Governance
- Assess data quality across tables and columns
- Update table and column descriptions for better documentation
- Monitor data freshness and completeness
- Generate data quality reports

### 🤖 AI-Powered Automation
- Natural language to SQL conversion
- Automated pipeline creation from business requirements
- Intelligent error diagnosis and resolution
- Context-aware data recommendations

## Prerequisites

1. **Python 3.10+** installed
2. **Access to a Keboola project** with appropriate permissions
3. **Keboola Storage API Token** (see setup instructions below)
4. **OpenAI API key** (or other LLM provider)

## Setup Instructions

### 1. Install Dependencies

```bash
pip3 install -U dspy[mcp] asyncio
```

### 2. Keboola Configuration

You'll need the following Keboola credentials:

- **KBC_STORAGE_API_URL**: Your Keboola region URL (e.g., `https://connection.keboola.com`)
- **KBC_STORAGE_TOKEN**: Your Keboola Storage API token
- **KBC_WORKSPACE_SCHEMA**: Your workspace schema (if using custom token)

#### Getting Your Keboola Credentials

1. **Storage API URL**: Based on your Keboola region:
   - AWS North America: `https://connection.keboola.com`
   - AWS Europe: `https://connection.eu-central-1.keboola.com`
   - Google Cloud EU: `https://connection.europe-west3.gcp.keboola.com`
   - Google Cloud US: `https://connection.us-east4.gcp.keboola.com`
   - Azure EU: `https://connection.north-europe.azure.keboola.com`

2. **Storage Token**: Create a token in your Keboola project:
   - Go to your Keboola project → Settings → API Tokens
   - Create a new token with appropriate permissions
   - For full access, use the Master Token

3. **Workspace Schema**: Only needed if using custom tokens
   - Go to Transformations → Sandboxes → Create New Sandbox
   - Note the workspace/dataset name

### 3. Environment Variables

Create a `.env` file or set environment variables:

```bash
export KBC_STORAGE_API_URL="https://connection.YOUR_REGION.keboola.com"
export KBC_STORAGE_TOKEN="your_keboola_storage_token"
export KBC_WORKSPACE_SCHEMA="your_workspace_schema"  # Optional if using Master Token
export OPENAI_API_KEY="your_openai_api_key"
```

### 4. Run the Demo

```bash
# 🎯 RECOMMENDED: Main demo entry point
python demo.py

# Advanced interactive demo with full features
python examples/interactive_demo.py

# Test that all tools are loading correctly
python examples/test_tools.py

# Or import and use agents directly in your code
python -c "from agents import KeboolaDataAnalyst; print('Ready!')"
```

## Available Keboola MCP Tools

The Keboola MCP Server provides these categories of tools:

### 📦 Storage Operations
- `list_buckets` - List all storage buckets
- `get_bucket` - Get bucket details
- `list_tables` - List tables in a bucket  
- `get_table` - Get table details and schema
- `query_table` - Execute SQL queries against data
- `update_table_description` - Update table documentation
- `update_bucket_description` - Update bucket documentation

### 🔧 Component Management
- `list_configs` - List component configurations
- `get_config` - Get component configuration details
- `create_config` - Create new component configurations
- `update_config` - Update existing configurations
- `find_component_id` - Search for components

### 🔄 SQL Transformations
- `create_sql_transformation` - Create SQL transformations
- `update_sql_transformation` - Update existing transformations
- `list_transformations` - List all transformations
- `get_sql_dialect` - Get workspace SQL dialect (Snowflake/BigQuery)

### ⚡ Job Management
- `start_job` - Trigger component/transformation jobs
- `retrieve_jobs` - List and filter jobs
- `get_job_detail` - Get detailed job information

### 🌊 Flow Orchestration
- `create_flow` - Create orchestration flows
- `list_flows` - List existing flows
- `get_flow` - Get flow details
- `update_flow` - Update flow configurations

### 📚 Documentation
- `docs_query` - Search Keboola documentation

## Example Use Cases

### 1. Customer Segmentation Analysis
```python
# The agent can:
# 1. Discover customer data tables
# 2. Analyze customer behavior patterns
# 3. Create RFM segmentation SQL transformation
# 4. Generate insights and recommendations
```

### 2. Data Pipeline Creation
```python
# The agent can:
# 1. Understand business requirements
# 2. Design optimal data flow architecture
# 3. Create necessary transformations
# 4. Set up monitoring and alerts
```

### 3. Data Quality Assessment
```python
# The agent can:
# 1. Scan all tables for quality issues
# 2. Identify missing or inconsistent data
# 3. Generate data quality reports
# 4. Suggest improvements and fixes
```

## Architecture

The demo follows this architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   DSPy Agent    │───▶│  Keboola MCP     │───▶│  Keboola        │
│   (AI Logic)    │    │  Server          │    │  Platform       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  LLM Provider   │    │  MCP Protocol    │    │  Data Storage   │
│  (OpenAI/etc)   │    │  (Tools/Calls)   │    │  (Snowflake/BQ) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Contributing

This demo is part of a collection of agent demos across various frameworks. To contribute:

1. Fork the repository
2. Create your feature branch
3. Add tests for new functionality
4. Submit a pull request

## Resources

- [DSPy Documentation](https://dspy.ai/)
- [Keboola MCP Server](https://github.com/keboola/mcp-server)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Keboola Platform](https://www.keboola.com/)

## License

This demo is provided under the MIT License. See LICENSE file for details. 