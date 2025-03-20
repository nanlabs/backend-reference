import pytest
from unittest.mock import patch
from langchain_core.runnables import RunnableConfig
from app.rag_graph.tools import create_web_search_tool


def test_create_web_search_tool_with_api_key():
    """Test creating web search tool with valid API key."""
    with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key'}):
        config = RunnableConfig()
        tool = create_web_search_tool(config)
        assert tool.api_key == 'test-key'
        assert tool.k == 3  # default max_results


def test_create_web_search_tool_custom_max_results():
    """Test creating web search tool with custom max_results."""
    with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key'}):
        config = RunnableConfig()
        tool = create_web_search_tool(config, max_results=5)
        assert tool.k == 5


def test_create_web_search_tool_missing_api_key():
    """Test creating web search tool without API key raises error."""
    with patch.dict('os.environ', {}, clear=True):
        config = RunnableConfig()
        with pytest.raises(ValueError) as exc_info:
            create_web_search_tool(config)
        assert "TAVILY_API_KEY environment variable is not set" in str(exc_info.value) 