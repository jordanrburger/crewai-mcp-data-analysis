# Quick Start Guide: DSPy + Keboola MCP Demo

Get up and running with AI-powered data analysis in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd dspy
pip install -r requirements.txt
```

### 2. Set Up Environment
Create a `.env` file in the parent directory with your Keboola credentials:

```bash
# Required
KBC_STORAGE_API_URL=https://connection.YOUR_REGION.keboola.com
KBC_STORAGE_TOKEN=your_keboola_storage_token
OPENAI_API_KEY=your_openai_api_key

# Optional (if using custom tokens)
KBC_WORKSPACE_SCHEMA=your_workspace_schema
```

### 3. Run the Demo
```bash
# 🎯 RECOMMENDED: Main demo entry point
python demo.py

# Advanced interactive demo
python examples/interactive_demo.py

# Test tool loading
python examples/test_tools.py
```

## 🎯 What You Can Do

### Data Analysis
- **Explore your data landscape** - Discover available datasets
- **Customer segmentation** - Analyze customer behavior patterns  
- **Revenue analysis** - Identify trends and opportunities
- **Data quality assessment** - Find and fix data issues

### Data Engineering
- **Build ETL pipelines** - Create data processing workflows
- **Customer 360 views** - Integrate customer data sources
- **Real-time analytics** - Set up streaming data pipelines
- **Data quality monitoring** - Automated quality checks

## 🛠️ Usage Examples

### Data Analyst Agent
```python
from agents import KeboolaDataAnalyst

# Initialize and explore data
analyst = KeboolaDataAnalyst()
await analyst.initialize()

# Ask questions about your data
result = await analyst.analyze_data("What data is available in my project?")

# Analyze customer behavior
insights = await analyst.analyze_data("Analyze customer behavior patterns")
```

### Pipeline Engineer Agent
```python
from agents import KeboolaPipelineEngineer

# Initialize and build pipelines
engineer = KeboolaPipelineEngineer()
await engineer.initialize()

# Create an ETL pipeline
pipeline = await engineer.design_pipeline("Create an ETL pipeline for sales data")

# Build Customer 360 view
customer_360 = await engineer.design_pipeline("Design a Customer 360 data pipeline")
```

## 🔧 Troubleshooting

### Environment Issues
- Make sure your `.env` file is in the parent directory (not in `/dspy`)
- Check that all required environment variables are set
- Verify your Keboola token has appropriate permissions

### Connection Issues
- Ensure your Keboola Storage API URL matches your region
- Check that your storage token is valid and not expired
- Verify network connectivity to Keboola servers

### Common Errors
- `ModuleNotFoundError`: Run `pip install -r requirements.txt`
- `Authentication failed`: Check your KBC_STORAGE_TOKEN
- `Invalid region`: Verify your KBC_STORAGE_API_URL

## 📚 Next Steps

1. **Explore the main demo** - Run `python demo.py`
2. **Try the interactive demo** - Run `python examples/interactive_demo.py`
3. **Customize for your data** - Modify prompts and logic for your specific needs
4. **Build your own agents** - Use these as templates for custom agents

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the [Keboola MCP Server docs](https://github.com/keboola/mcp-server)
- Explore [DSPy documentation](https://dspy.ai/) 