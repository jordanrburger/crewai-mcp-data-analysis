"""
Keboola MCP Server Integration for LangChain

This module provides integration between Keboola MCP Server and LangChain,
allowing LangChain agents to use Keboola data platform tools.
"""

import os
import asyncio
import json
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from pydantic import BaseModel, Field


class KeboolaMCPTool(BaseTool):
    """A LangChain tool that wraps a Keboola MCP Server tool."""
    
    name: str = Field(description="The name of the tool")
    description: str = Field(description="Description of the tool") 
    mcp_tool_name: str = Field(description="The name of the MCP tool")
    mcp_tool_description: str = Field(description="Description of the MCP tool")
    mcp_tool_schema: Dict[str, Any] = Field(description="JSON schema for the MCP tool")
    server_params: StdioServerParameters = Field(description="MCP server parameters")
    
    class Config:
        arbitrary_types_allowed = True
    
    def _run(
        self,
        tool_input: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs
    ) -> str:
        """Execute the MCP tool synchronously."""
        try:
            # Handle both string input and keyword arguments
            arguments = {}
            
            # Priority: kwargs > parsed tool_input > raw tool_input
            if kwargs:
                # LangChain is passing named arguments - use them directly
                arguments = kwargs
            elif tool_input:
                # If tool_input is provided, try to parse it as JSON first
                try:
                    parsed_input = json.loads(tool_input)
                    if isinstance(parsed_input, dict):
                        arguments = parsed_input
                    else:
                        # If it's not a dict, treat as a simple query
                        arguments = {"query": str(parsed_input)}
                except json.JSONDecodeError:
                    # If not JSON, treat as a simple string query
                    arguments = {"query": tool_input}
            
            # Remove any None values from arguments
            arguments = {k: v for k, v in arguments.items() if v is not None}
            
            # Check if there's already an event loop running
            try:
                loop = asyncio.get_running_loop()
                # If there is, we need to run in a new thread
                import concurrent.futures
                
                def run_async():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        return new_loop.run_until_complete(self._arun_with_args(arguments, run_manager))
                    finally:
                        new_loop.close()
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_async)
                    return future.result(timeout=30)  # 30 second timeout
                    
            except RuntimeError:
                # No event loop running, safe to use asyncio.run
                return asyncio.run(self._arun_with_args(arguments, run_manager))
                
        except Exception as e:
            return f"Error running MCP tool {self.mcp_tool_name}: {str(e)}"
    
    async def _arun(
        self,
        tool_input: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs
    ) -> str:
        """Execute the MCP tool asynchronously."""
        # Handle both string input and keyword arguments
        arguments = {}
        
        # Priority: kwargs > parsed tool_input > raw tool_input  
        if kwargs:
            # LangChain is passing named arguments - use them directly
            arguments = kwargs
        elif tool_input:
            # If tool_input is provided, try to parse it as JSON first
            try:
                parsed_input = json.loads(tool_input)
                if isinstance(parsed_input, dict):
                    arguments = parsed_input
                else:
                    # If it's not a dict, treat as a simple query
                    arguments = {"query": str(parsed_input)}
            except json.JSONDecodeError:
                # If not JSON, treat as a simple string query
                arguments = {"query": tool_input}
        
        # Remove any None values from arguments
        arguments = {k: v for k, v in arguments.items() if v is not None}
        
        return await self._arun_with_args(arguments, run_manager)
    
    async def _arun_with_args(
        self,
        arguments: Dict[str, Any],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the MCP tool asynchronously with parsed arguments."""
        try:
            # Get the schema properties to understand what arguments this tool accepts
            schema_properties = self.mcp_tool_schema.get('properties', {})
            
            # Handle tools that require random_string parameter when no arguments provided
            if not arguments and 'random_string' in schema_properties:
                arguments = {"random_string": "dummy"}
            
            # Filter out arguments that the tool doesn't accept
            if schema_properties:
                # Only keep arguments that are defined in the schema
                filtered_arguments = {k: v for k, v in arguments.items() if k in schema_properties}
                # If we filtered out everything and had a 'query' argument, 
                # try to map it to the first string parameter in the schema
                if not filtered_arguments and 'query' in arguments:
                    # Find the first string parameter in the schema
                    for param_name, param_def in schema_properties.items():
                        if isinstance(param_def, dict) and param_def.get('type') == 'string':
                            filtered_arguments[param_name] = arguments['query']
                            break
                arguments = filtered_arguments
            
            # Debug logging
            if os.getenv('DEBUG_MCP_TOOLS'):
                print(f"Calling MCP tool {self.mcp_tool_name} with arguments: {arguments}")
                print(f"Schema properties: {list(schema_properties.keys()) if schema_properties else 'None'}")
            
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Call the MCP tool
                    result = await session.call_tool(self.mcp_tool_name, arguments)
                    
                    # Extract content from the result
                    if hasattr(result, 'content') and result.content:
                        if isinstance(result.content, list):
                            return '\n'.join(str(item.text) if hasattr(item, 'text') else str(item) for item in result.content)
                        else:
                            return str(result.content)
                    else:
                        return str(result)
                        
        except Exception as e:
            error_msg = f"Error executing Keboola MCP tool {self.mcp_tool_name}: {str(e)}"
            if os.getenv('DEBUG_MCP_TOOLS'):
                print(f"Error details: {error_msg}")
                print(f"Arguments were: {arguments}")
                print(f"Schema properties: {list(schema_properties.keys()) if schema_properties else 'None'}")
            return error_msg


class KeboolaMCPToolLoader:
    """Loads Keboola MCP Server tools as LangChain tools."""
    
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="uvx",
            args=["--from", "keboola-mcp-server@1.0.0", "keboola-mcp-server"],
            env={
                "KBC_STORAGE_API_URL": os.getenv("KBC_STORAGE_API_URL"),
                "KBC_STORAGE_TOKEN": os.getenv("KBC_STORAGE_TOKEN"),
                "KBC_WORKSPACE_SCHEMA": os.getenv("KBC_WORKSPACE_SCHEMA", "")
            }
        )
    
    async def load_tools(self) -> List[KeboolaMCPTool]:
        """Load all available Keboola MCP tools as LangChain tools."""
        tools = []
        
        try:
            # Use asyncio.wait_for for timeout
            tools = await asyncio.wait_for(
                self._load_tools_impl(), 
                timeout=45.0
            )
                        
        except asyncio.TimeoutError:
            print("Timeout loading Keboola MCP tools - server may be unresponsive")
        except Exception as e:
            print(f"Error loading Keboola MCP tools: {e}")
            import traceback
            traceback.print_exc()
            
        return tools
    
    async def _load_tools_impl(self) -> List[KeboolaMCPTool]:
        """Internal implementation for loading tools."""
        tools = []
        
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Get available tools
                tools_response = await session.list_tools()
                
                for mcp_tool in tools_response.tools:
                    try:
                        # Handle inputSchema - it might be a dict or a Pydantic model
                        if hasattr(mcp_tool, 'inputSchema') and mcp_tool.inputSchema:
                            if hasattr(mcp_tool.inputSchema, 'model_dump'):
                                # It's a Pydantic model
                                schema = mcp_tool.inputSchema.model_dump()
                            elif isinstance(mcp_tool.inputSchema, dict):
                                # It's already a dict
                                schema = mcp_tool.inputSchema
                            else:
                                # Convert to dict
                                schema = dict(mcp_tool.inputSchema) if mcp_tool.inputSchema else {}
                        else:
                            schema = {}
                        
                        langchain_tool = KeboolaMCPTool(
                            name=f"keboola_{mcp_tool.name}",
                            description=f"Keboola MCP Tool: {mcp_tool.description or f'Keboola tool: {mcp_tool.name}'}",
                            mcp_tool_name=mcp_tool.name,
                            mcp_tool_description=mcp_tool.description or f"Keboola tool: {mcp_tool.name}",
                            mcp_tool_schema=schema,
                            server_params=self.server_params
                        )
                        tools.append(langchain_tool)
                    except Exception as tool_error:
                        print(f"Error creating tool {mcp_tool.name}: {tool_error}")
                        continue
                
                print(f"Successfully loaded {len(tools)} Keboola MCP tools")
                
        return tools
    
    def load_tools_sync(self) -> List[KeboolaMCPTool]:
        """Synchronous wrapper for loading tools."""
        try:
            # Check if there's already an event loop running
            loop = asyncio.get_running_loop()
            # If there is, we need to run in a new thread
            import concurrent.futures
            
            def run_async():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(self.load_tools())
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async)
                return future.result(timeout=60)  # 60 second timeout for loading
                
        except RuntimeError:
            # No event loop running, safe to use asyncio.run
            return asyncio.run(self.load_tools())
        except Exception as e:
            print(f"Error in load_tools_sync: {e}")
            return []


# Convenience function
def get_keboola_tools() -> List[KeboolaMCPTool]:
    """Get all Keboola MCP tools as LangChain tools."""
    loader = KeboolaMCPToolLoader()
    return loader.load_tools_sync() 