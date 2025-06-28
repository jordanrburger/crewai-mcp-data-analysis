# LangChain Data Analyst Agent with Keboola MCP Integration

A powerful data analyst agent built with LangChain that integrates with Keboola MCP Server and includes additional analysis tools for comprehensive data analysis capabilities.

## 🚀 Features

### Keboola Data Platform Integration
- **Data Storage Access**: Query and analyze data stored in Keboola buckets and tables
- **Transformation Management**: Create and manage data transformations
- **Pipeline Monitoring**: Monitor data pipeline jobs and workflows
- **Component Configuration**: Retrieve and manage component configurations
- **SQL Execution**: Execute SQL queries against your data warehouse

### Additional Analysis Tools
- **Web Search**: Research and gather context using DuckDuckGo
- **Financial Data**: Real-time stock market data and analysis via Yahoo Finance
- **Data Visualization**: Create charts and visualizations with Plotly
- **Statistical Analysis**: Perform correlation studies and descriptive statistics
- **Web Scraping**: Extract data from web pages
- **Python Execution**: Run custom Python code for advanced analysis
- **Wikipedia Research**: Access encyclopedic information

### LangChain Features
- **Conversational Memory**: Maintains context across interactions
- **ReAct Agent**: Uses reasoning and acting pattern for complex queries
- **Streaming Responses**: Real-time response streaming for better UX
- **Error Handling**: Robust error handling and recovery
- **Tool Integration**: Seamless integration of multiple tool types

## 📋 Prerequisites

1. **Keboola Connection Project** with:
   - Storage API URL
   - Storage API Token
   - (Optional) Workspace Schema

2. **OpenAI API Key** for the language model

3. **Python 3.8+** with pip

## 🛠️ Installation

1. **Clone or navigate to the langchain directory**:
   ```bash
   cd agent-demos/langchain
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the parent directory (`agent-demos/.env`):
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Keboola Configuration
   KBC_STORAGE_API_URL=https://connection.keboola.com
   KBC_STORAGE_TOKEN=your_keboola_token_here
   KBC_WORKSPACE_SCHEMA=your_workspace_schema  # Optional
   ```

## 🎯 Usage

### Quick Start

Run the interactive demo:
```bash
python3 demo.py
```

Or run a quick test:
```bash
python3 demo.py --test
```

### Programmatic Usage

```python
from data_analyst_agent import DataAnalystAgent

# Initialize the agent
agent = DataAnalystAgent(
    model="gpt-4o",
    temperature=0.1,
    verbose=True
)

# Perform analysis
result = agent.analyze("What data is available in my Keboola project?")
print(result)

# Get tool information
tools_info = agent.get_tool_info()
print(tools_info)
```

### Advanced Configuration

```python
# Custom configuration
agent = DataAnalystAgent(
    model="gpt-4o-mini",        # Use different model
    temperature=0.3,            # More creative responses
    max_tokens=2000,           # Shorter responses
    verbose=False,             # Quiet mode
    memory_window=20           # Remember more context
)
```

## 📊 Example Queries

### Keboola Data Exploration
```
"What buckets and tables are available in my Keboola project?"
"Show me the schema and sample data from the 'customers' table"
"What transformations are currently configured?"
"Check the status of recent pipeline jobs"
```

### Financial Analysis
```
"Get current stock price and metrics for Apple (AAPL)"
"Compare the performance of TSLA vs AAPL over the last month"
"Analyze the financial health of Microsoft based on key metrics"
```

### Market Research
```
"Search for recent news about artificial intelligence in healthcare"
"What are the latest trends in data engineering for 2024?"
"Find information about cloud computing adoption rates"
```

### Data Analysis
```
"Create a visualization of sales data by region"
"Perform correlation analysis on customer demographics"
"Generate summary statistics for revenue data"
```

## 🔧 Architecture

### Core Components

1. **DataAnalystAgent**: Main agent class that orchestrates all functionality
2. **KeboolaMCPToolLoader**: Loads Keboola MCP Server tools as LangChain tools
3. **Additional Tools**: Provides supplementary analysis capabilities
4. **LangChain Integration**: Uses ReAct agent with conversational memory

### Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| **Keboola MCP** | 31 tools | Complete Keboola platform integration |
| **Search & Research** | DuckDuckGo, Wikipedia | Web search and research capabilities |
| **Financial** | Yahoo Finance | Stock market data and analysis |
| **Visualization** | Plotly | Interactive charts and graphs |
| **Analysis** | Statistical tools | Descriptive stats and correlations |
| **Development** | Python executor | Custom code execution |
| **Web** | Web scraping | Extract data from websites |

### Data Flow

```
User Query → LangChain Agent → Tool Selection → Tool Execution → Response Generation
     ↑                                                                    ↓
Conversation Memory ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←← Streaming Response
```

## 🎛️ Configuration Options

### Model Options
- `gpt-4o`: Most capable, higher cost
- `gpt-4o-mini`: Balanced performance and cost
- `gpt-3.5-turbo`: Fastest, most economical

### Agent Parameters
- `temperature`: Controls response creativity (0.0-1.0)
- `max_tokens`: Maximum response length
- `verbose`: Show detailed reasoning steps
- `memory_window`: Number of conversation turns to remember

### Tool Configuration
Tools are automatically loaded based on available credentials and dependencies.

## 🔍 Troubleshooting

### Common Issues

1. **Keboola Tools Not Loading**
   ```
   ⚠️ Failed to load Keboola MCP tools: [error]
   ```
   - Verify `KBC_STORAGE_API_URL` and `KBC_STORAGE_TOKEN` in `.env`
   - Check network connectivity to Keboola
   - Ensure token has proper permissions

2. **OpenAI API Errors**
   ```
   Error: OpenAI API key not found
   ```
   - Set `OPENAI_API_KEY` in `.env` file
   - Verify API key is valid and has credits

3. **Module Import Errors**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   - Run `pip3 install -r requirements.txt`
   - Ensure you're in the correct directory

4. **Tool Execution Errors**
   - Check internet connectivity for web-based tools
   - Verify data format for analysis tools
   - Review tool-specific error messages in verbose mode

### Debug Mode

Enable detailed logging:
```python
agent = DataAnalystAgent(verbose=True)
```

### Tool Testing

Test individual tool categories:
```python
from keboola_mcp_tools import get_keboola_tools
from additional_tools import get_additional_tools

# Test Keboola tools
keboola_tools = get_keboola_tools()
print(f"Loaded {len(keboola_tools)} Keboola tools")

# Test additional tools
additional_tools = get_additional_tools()
print(f"Loaded {len(additional_tools)} additional tools")
```

## 📈 Performance Tips

1. **Use appropriate model**: `gpt-4o-mini` for most tasks, `gpt-4o` for complex analysis
2. **Optimize memory window**: Smaller window for faster responses
3. **Batch related queries**: Ask multiple related questions in one session
4. **Use specific queries**: More specific questions get better results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Keboola MCP agent demos collection.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the [Keboola MCP Server documentation](https://github.com/keboola/mcp-server)
3. Consult the [LangChain documentation](https://python.langchain.com/)
4. Open an issue in the repository

---

**Built with ❤️ using LangChain and Keboola MCP Server** 