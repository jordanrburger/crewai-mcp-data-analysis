# Agent Demos

A comprehensive collection of AI agent implementations using various agentic frameworks, with a focus on data analysis and Keboola MCP Server integration.

## 🚀 Overview

This repository demonstrates how to build powerful AI agents using different frameworks:

- **CrewAI**: Multi-agent collaboration for complex data analysis tasks
- **LangChain**: Flexible agent framework with extensive tool integration
- **DSPy**: Programming foundation models with optimized prompting

All demos integrate with the [Keboola MCP Server](https://github.com/keboola/mcp-server) for seamless data platform operations.

## 📁 Repository Structure

```
agent-demos/
├── crew-ai/           # CrewAI-based agents
├── langchain/         # LangChain agent implementations  
├── dspy/              # DSPy framework examples
├── .env.template      # Environment variables template
└── README.md          # This file
```

## 🛠️ Framework Comparisons

| Framework | Strengths | Best For |
|-----------|-----------|----------|
| **CrewAI** | Multi-agent collaboration, role-based agents | Complex workflows requiring specialized roles |
| **LangChain** | Extensive tool ecosystem, mature framework | General-purpose agents with many integrations |
| **DSPy** | Optimized prompting, systematic approach | Research and performance-critical applications |

## 🔧 Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd agent-demos
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.template .env
   # Edit .env with your API keys and configuration
   ```

3. **Install dependencies for each framework:**
   ```bash
   # CrewAI
   cd crew-ai && pip install -r requirements.txt

   # LangChain  
   cd ../langchain && pip install -r requirements.txt

   # DSPy
   cd ../dspy && pip install -r requirements.txt
   ```

## 🎯 Quick Start

### CrewAI Demo
```bash
cd crew-ai
python demo.py
```

### LangChain Demo
```bash
cd langchain
python demo.py
```

### DSPy Demo
```bash
cd dspy
python demo.py
```

## 🔌 Keboola MCP Integration

All frameworks integrate with Keboola MCP Server for:

- **Data Access**: Query tables and buckets
- **Transformations**: Create and manage data transformations
- **Job Management**: Monitor and execute data pipelines
- **Metadata**: Access component and configuration information

### Required Environment Variables

```bash
KBC_STORAGE_API_URL=https://connection.keboola.com
KBC_STORAGE_TOKEN=your_keboola_token
OPENAI_API_KEY=your_openai_key
```

## 📊 Use Cases

### Data Analysis
- Customer segmentation and behavior analysis
- Revenue forecasting and trend analysis
- Operational metrics and KPI tracking
- Churn prediction and retention analysis

### Business Intelligence
- Automated report generation
- Cross-platform data correlation
- Real-time dashboard updates
- Performance monitoring

### Data Engineering
- Pipeline orchestration
- Data quality monitoring
- Transformation optimization
- Schema management

## 🔍 Climbing Gym Analysis Example

This repository includes comprehensive examples for analyzing climbing gym data, including:

- **Program Attendance Analysis**: Track attendance by location and department
- **Yoga Class Popularity**: Identify the most popular yoga classes
- **ROI Analysis**: Calculate return on investment considering instructor pay rates and class revenue
- **Youth Program Metrics**: Analyze youth class attendance and coach-to-kid ratios
- **Financial Performance**: Join labor data with revenue data for comprehensive analysis

See the individual framework directories for specific implementations.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Keboola](https://www.keboola.com/) for the MCP Server
- [CrewAI](https://github.com/joaomdmoura/crewAI) team
- [LangChain](https://github.com/langchain-ai/langchain) community
- [DSPy](https://github.com/stanfordnlp/dspy) researchers

## 📞 Support

For questions and support:
- Open an issue in this repository
- Check the individual framework documentation
- Review the Keboola MCP Server documentation 