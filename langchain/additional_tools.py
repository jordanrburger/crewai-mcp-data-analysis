"""
Additional Tools for Data Analyst Agent

This module provides additional useful tools beyond Keboola MCP tools,
including web search, financial data, Wikipedia, and data visualization tools.
"""

import os
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, Any
from langchain.tools import BaseTool, Tool
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field
import yfinance as yf
from datetime import datetime, timedelta


class FinancialDataTool(BaseTool):
    """Tool for fetching financial data using yfinance."""
    
    name: str = "financial_data"
    description: str = "Fetch financial data for stocks, ETFs, or other securities. Input should be a ticker symbol (e.g., 'AAPL', 'GOOGL')."
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Fetch financial data for a given ticker."""
        try:
            ticker = query.strip().upper()
            stock = yf.Ticker(ticker)
            
            # Get basic info
            info = stock.info
            
            # Get recent price data (last 30 days)
            hist = stock.history(period="1mo")
            
            # Get current price
            current_price = hist['Close'].iloc[-1] if not hist.empty else "N/A"
            
            # Calculate basic metrics
            if not hist.empty and len(hist) > 1:
                price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[-2]
                price_change_pct = (price_change / hist['Close'].iloc[-2]) * 100
                
                high_52w = hist['High'].max()
                low_52w = hist['Low'].min()
                avg_volume = hist['Volume'].mean()
            else:
                price_change = price_change_pct = high_52w = low_52w = avg_volume = "N/A"
            
            result = {
                "ticker": ticker,
                "company_name": info.get("longName", "N/A"),
                "current_price": current_price,
                "price_change": price_change,
                "price_change_percent": price_change_pct,
                "52_week_high": high_52w,
                "52_week_low": low_52w,
                "average_volume": avg_volume,
                "market_cap": info.get("marketCap", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A")
            }
            
            return json.dumps(result, indent=2, default=str)
            
        except Exception as e:
            return f"Error fetching financial data for {query}: {str(e)}"


class DataVisualizationTool(BaseTool):
    """Tool for creating data visualizations."""
    
    name: str = "data_visualization"
    description: str = "Create data visualizations. Input should be JSON with 'data' (list of dicts), 'chart_type' (bar, line, scatter, pie), and 'title'."
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Create a data visualization."""
        try:
            params = json.loads(query)
            data = params.get("data", [])
            chart_type = params.get("chart_type", "bar")
            title = params.get("title", "Data Visualization")
            
            if not data:
                return "Error: No data provided for visualization"
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Create visualization based on type
            if chart_type == "bar":
                if len(df.columns) >= 2:
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=title)
                else:
                    return "Error: Bar chart requires at least 2 columns"
                    
            elif chart_type == "line":
                if len(df.columns) >= 2:
                    fig = px.line(df, x=df.columns[0], y=df.columns[1], title=title)
                else:
                    return "Error: Line chart requires at least 2 columns"
                    
            elif chart_type == "scatter":
                if len(df.columns) >= 2:
                    fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title=title)
                else:
                    return "Error: Scatter plot requires at least 2 columns"
                    
            elif chart_type == "pie":
                if len(df.columns) >= 2:
                    fig = px.pie(df, values=df.columns[1], names=df.columns[0], title=title)
                else:
                    return "Error: Pie chart requires at least 2 columns"
            else:
                return f"Error: Unsupported chart type '{chart_type}'. Supported types: bar, line, scatter, pie"
            
            # Save the plot
            filename = f"visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(filename)
            
            return f"Visualization created successfully and saved as '{filename}'. Chart type: {chart_type}, Data points: {len(data)}"
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for visualization parameters"
        except Exception as e:
            return f"Error creating visualization: {str(e)}"


class DataAnalysisTool(BaseTool):
    """Tool for performing basic data analysis operations."""
    
    name: str = "data_analysis"
    description: str = "Perform basic data analysis on datasets. Input should be JSON with 'data' (list of dicts) and 'operation' (describe, correlate, summarize)."
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Perform data analysis operations."""
        try:
            params = json.loads(query)
            data = params.get("data", [])
            operation = params.get("operation", "describe")
            
            if not data:
                return "Error: No data provided for analysis"
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            if operation == "describe":
                # Basic statistical description
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    description = df[numeric_cols].describe()
                    return f"Dataset Description:\n{description.to_string()}"
                else:
                    return "No numeric columns found for statistical description"
                    
            elif operation == "correlate":
                # Correlation analysis
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 1:
                    correlation = df[numeric_cols].corr()
                    return f"Correlation Matrix:\n{correlation.to_string()}"
                else:
                    return "Need at least 2 numeric columns for correlation analysis"
                    
            elif operation == "summarize":
                # General summary
                summary = {
                    "total_rows": len(df),
                    "total_columns": len(df.columns),
                    "column_names": list(df.columns),
                    "data_types": df.dtypes.to_dict(),
                    "missing_values": df.isnull().sum().to_dict(),
                    "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
                    "categorical_columns": list(df.select_dtypes(include=['object']).columns)
                }
                return json.dumps(summary, indent=2, default=str)
            else:
                return f"Error: Unsupported operation '{operation}'. Supported operations: describe, correlate, summarize"
                
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for analysis parameters"
        except Exception as e:
            return f"Error performing data analysis: {str(e)}"


class WebScrapingTool(BaseTool):
    """Tool for basic web scraping and data extraction."""
    
    name: str = "web_scraping"
    description: str = "Scrape data from web pages. Input should be a URL to scrape basic text content from."
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Scrape basic content from a web page."""
        try:
            from bs4 import BeautifulSoup
            
            url = query.strip()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Extract paragraphs
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs[:5]])  # First 5 paragraphs
            
            # Extract headings
            headings = []
            for i in range(1, 4):  # h1, h2, h3
                headers = soup.find_all(f'h{i}')
                headings.extend([h.get_text().strip() for h in headers[:3]])  # First 3 of each
            
            result = {
                "url": url,
                "title": title_text,
                "headings": headings[:10],  # First 10 headings
                "content_preview": content[:1000] + "..." if len(content) > 1000 else content
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error scraping web page {query}: {str(e)}"


def get_additional_tools():
    """Get all additional tools for the data analyst agent."""
    
    # Initialize tools
    search_tool = DuckDuckGoSearchRun()
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    financial_tool = FinancialDataTool()
    visualization_tool = DataVisualizationTool()
    analysis_tool = DataAnalysisTool()
    scraping_tool = WebScrapingTool()
    
    # Create a Python code execution tool
    python_tool = Tool(
        name="python_executor",
        description="Execute Python code for data analysis. Input should be valid Python code as a string.",
        func=lambda code: exec_python_code(code)
    )
    
    return [
        search_tool,
        wikipedia_tool,
        financial_tool,
        visualization_tool,
        analysis_tool,
        scraping_tool,
        python_tool
    ]


def exec_python_code(code: str) -> str:
    """Safely execute Python code for data analysis."""
    try:
        # Create a restricted environment
        allowed_modules = {
            'pandas': pd,
            'numpy': np,
            'matplotlib': plt,
            'seaborn': sns,
            'plotly': px,
            'json': json,
            'datetime': datetime,
            'math': __import__('math'),
            'statistics': __import__('statistics')
        }
        
        # Capture output
        import io
        import sys
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        
        # Execute code with restricted globals
        with redirect_stdout(output):
            exec(code, {"__builtins__": {}, **allowed_modules})
        
        result = output.getvalue()
        return result if result else "Code executed successfully (no output)"
        
    except Exception as e:
        return f"Error executing Python code: {str(e)}" 