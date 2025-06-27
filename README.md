# CrewAI Data Analysis Crew with Keboola MCP Server

This project demonstrates how to create a powerful CrewAI crew that integrates with the **Keboola MCP Server** for advanced data analysis operations. The crew consists of specialized AI agents that can interact with your Keboola project through the Model Context Protocol (MCP).

## 🚀 Features

- **Data Explorer Agent**: Discovers and explores data structures, schemas, and relationships
- **Data Analyst Agent**: Performs advanced SQL analysis, generates insights, and creates reports  
- **Pipeline Engineer Agent**: Creates and optimizes data transformations and workflows
- **Real Keboola Integration**: Uses the official Keboola MCP Server and CrewAI MCP Toolbox
- **Production Ready**: Connects to your actual Keboola project with proper authentication

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.10+** installed
2. **A Keboola project** with admin access
3. **OpenAI API key** for the CrewAI agents
4. **UV package manager** installed (for MCP server execution)

### Installing UV

**macOS/Linux:**
```bash
# Using Homebrew
brew install uv

# Or using the installer script
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
# Using the installer script
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

## 🛠️ Setup

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd crewai-mcp
pip3 install -r requirements.txt
```

### 2. Configure Keboola Credentials

You need to obtain the following from your Keboola project:

#### KBC_STORAGE_TOKEN
Your Keboola Storage API token. Get this from:
1. Go to your Keboola project
2. Navigate to **Users & Settings** → **API Tokens**
3. Create a new token or use your master token

#### KBC_WORKSPACE_SCHEMA  
Your workspace schema for SQL queries:
1. Go to **Transformations** → **Workspace**
2. Create a workspace if you don't have one
3. Copy the workspace schema name
4. **Important**: Check "Grant read-only access to all Project data" when creating

#### KBC_STORAGE_API_URL
Your Keboola API URL based on your region:

| Region | API URL |
|--------|---------|
| AWS North America | `https://connection.keboola.com` |
| AWS Europe | `https://connection.eu-central-1.keboola.com` |
| Google Cloud EU | `https://connection.europe-west3.gcp.keboola.com` |
| Google Cloud US | `https://connection.us-east4.gcp.keboola.com` |
| Azure EU | `https://connection.north-europe.azure.keboola.com` |

### 3. Create Environment File

Copy the template and fill in your credentials:

```bash
cp env_template.txt .env
```

Edit `.env` with your actual values:

```bash
# OpenAI API Key for CrewAI agents
OPENAI_API_KEY=your_openai_api_key_here

# Keboola Configuration  
KBC_STORAGE_TOKEN=your_keboola_token_here
KBC_WORKSPACE_SCHEMA=your_workspace_schema_here
KBC_STORAGE_API_URL=https://connection.keboola.com

# Optional: Other LLM providers
# ANTHROPIC_API_KEY=your_anthropic_key_here
```

## 🎯 Usage

### Basic Usage

Run the data analysis crew:

```bash
python data_analysis_crew.py
```

This will:
1. Connect to your Keboola project via MCP
2. Discover available Keboola tools
3. Create three specialized agents
4. Execute a comprehensive data analysis workflow

### What the Crew Does

The crew executes three main tasks sequentially:

1. **Data Exploration** (Data Explorer Agent)
   - Lists all buckets and tables
   - Examines data schemas and quality
   - Documents relationships between datasets

2. **Data Analysis** (Data Analyst Agent)  
   - Calculates business metrics and KPIs
   - Performs statistical analysis
   - Identifies trends and anomalies
   - Executes custom SQL queries

3. **Pipeline Optimization** (Pipeline Engineer Agent)
   - Reviews existing transformations
   - Analyzes job performance
   - Creates new transformations if needed
   - Provides optimization recommendations

### Available Keboola Tools

The MCP integration provides access to these Keboola capabilities:

| Category | Tools | Description |
|----------|-------|-------------|
| **Storage** | `retrieve_buckets`, `get_bucket_detail`, `retrieve_bucket_tables`, `get_table_detail` | Explore data structure |
| **SQL** | `query_table`, `get_sql_dialect` | Execute queries and analysis |
| **Components** | `retrieve_components`, `get_component_details`, `create_sql_transformation` | Manage transformations |
| **Jobs** | `retrieve_jobs`, `get_job_detail`, `start_job` | Monitor and execute workflows |
| **Documentation** | `docs_query` | Search Keboola documentation |

## 🔧 Customization

### Custom Analysis Objectives

You can customize the analysis by modifying the `custom_objective` parameter:

```python
result = await analysis_crew.run_analysis(
    custom_objective="Focus on customer segmentation and retention analysis"
)
```

### Adding Custom Agents

Create additional specialized agents:

```python
def create_custom_agent(self, keboola_tools: List) -> Agent:
    return Agent(
        role="Custom Specialist", 
        goal="Your specific goal",
        backstory="Your agent's background",
        tools=keboola_tools,
        verbose=True
    )
```

### Modifying Tasks

Customize the analysis workflow by editing the task descriptions in the respective `create_*_task()` methods.

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Authentication Errors** | Verify `KBC_STORAGE_TOKEN` is valid and has proper permissions |
| **Workspace Issues** | Confirm `KBC_WORKSPACE_SCHEMA` exists and has data access |
| **Connection Timeout** | Check network connectivity and API URL |
| **No Tools Found** | Ensure UV is installed and MCP server can start |

### Debug Mode

Enable verbose logging by setting agents to `verbose=True` (already enabled by default).

### Testing MCP Connection

Test your Keboola MCP connection separately:

```bash
# Test the MCP server directly
uvx keboola_mcp_server --help
```

## 📚 References

- [Keboola MCP Server Documentation](https://github.com/keboola/mcp-server/)
- [CrewAI MCP Integration](https://docs.crewai.com/mcp/overview)
- [CrewAI MCP Toolbox](https://pypi.org/project/crewai-mcp-toolbox/)
- [Keboola Help - MCP Server](https://help.keboola.com/ai/mcp-server/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For issues related to:
- **Keboola MCP Server**: [GitHub Issues](https://github.com/keboola/mcp-server/issues)
- **CrewAI**: [CrewAI Documentation](https://docs.crewai.com/)
- **This Project**: Open an issue in this repository

---

**Happy Data Analysis! 🎉** 