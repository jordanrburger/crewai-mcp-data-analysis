"""
Keboola MCP + DSPy Agents

This package contains AI agents that integrate with Keboola data platform
through the Model Context Protocol (MCP) using DSPy framework.
"""

from .data_analyst_agent import KeboolaDataAnalyst
from .pipeline_engineer_agent import KeboolaPipelineEngineer

__all__ = ['KeboolaDataAnalyst', 'KeboolaPipelineEngineer'] 