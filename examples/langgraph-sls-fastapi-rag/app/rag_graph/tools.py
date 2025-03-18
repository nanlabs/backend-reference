from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig


def create_web_search_tool(config: RunnableConfig):
    web_search_tool = TavilySearchResults(k=3)
    return web_search_tool