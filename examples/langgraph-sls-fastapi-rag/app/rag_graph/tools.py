from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
import os
from typing import Optional


def create_web_search_tool(config: RunnableConfig, max_results: Optional[int] = 3):
    """
    Creates a web search tool using the Tavily Search API.
    
    Args:
        config: Configuration for the runnable.
        max_results: Maximum number of search results to return (default: 3).
        
    Returns:
        An instance of TavilySearchResults configured with the provided parameters.
        
    Raises:
        ValueError: If TAVILY_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY environment variable is not set. "
            "Please set it to use the web search tool."
        )
    
    web_search_tool = TavilySearchResults(api_key=api_key, k=max_results)
    return web_search_tool