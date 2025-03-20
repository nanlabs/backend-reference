import logging
import os
from datetime import datetime, timezone

from langchain_aws import ChatBedrock
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from app.rag_graph.state import State
from app.shared.utils import format_docs, get_message_text

from .configuration import Configuration
from .retrieval import make_retriever
from .tools import create_web_search_tool


logger = logging.getLogger(__name__)

async def create_query(
    state: State, *, config: RunnableConfig
) -> dict[str, list[str]]:
    """Extract the latest message from the state and format it into a query.
    
    Args:
        state (State): The current state containing messages.
        config (RunnableConfig): Configuration for the query creation process.
        
    Returns:
        dict[str, list[str]]: A dictionary with a single key "queries" containing the query.
    """
    if not state.messages:
        logger.warning("No messages in state to create query from")
        return {"queries": [""]}
    message = state.messages[-1]
    query = get_message_text(message)
    return {"queries": [query]}


async def retrieve(
    state: State, *, config: RunnableConfig
) -> dict[str, list[Document]]:
    """Retrieve documents based on the latest query in the state.

    This function takes the current state and configuration, uses the latest query
    from the state to retrieve relevant documents using the retriever, and returns
    the retrieved documents.

    Args:
        state (State): The current state containing queries and the retriever.
        config (RunnableConfig | None, optional): Configuration for the retrieval process.

    Returns:
        dict[str, list[Document]]: A dictionary with a single key "retrieved_docs"
        containing a list of retrieved Document objects.
    """
    with make_retriever(config) as retriever:
        response = await retriever.ainvoke(state.queries[-1], config)
        logger.info(f"Retrieved documents for query: {state.queries[-1]}")
        logger.info(f"Retrieved documents: {response}")

        return {"retrieved_docs": response}


def web_search(
    state: State, *, config: RunnableConfig
) -> dict[str, list[str]]:
    """
    Web search based on the re-phrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with appended web results
    """
    if not state.queries:
        logger.warning("No queries in state for web search.")
        return {"web_search_results": []}

    if not state.queries:
        logger.warning("No queries in state for web search.")
        return {"web_search_results": []}
    logging.info("Performing web search for query: %s", state.queries[-1])
    question = state.queries[-1]

    # Web search
    web_search_tool = create_web_search_tool(config)
    docs = web_search_tool.invoke({"query": question})

    logging.debug("Web search results obtained: %s", docs)
    return {"web_search_results": docs}

async def respond(
    state: State, *, config: RunnableConfig
) -> dict[str, list[BaseMessage]]:
    """Call the LLM powering our "agent"."""
    configuration = Configuration.from_runnable_config(config)
    # Feel free to customize the prompt, model, and other logic!
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", configuration.response_system_prompt),
            ("placeholder", "{messages}"),
        ]
    )

    llm = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        region_name=os.environ.get("AWS_REGION", "us-west-2"),
        model_kwargs=dict(temperature=0))

    retrieved_docs = format_docs(state.retrieved_docs)
    message_value = await prompt.ainvoke(
        {
            "messages": state.messages,
            "retrieved_docs": retrieved_docs,
            "system_time": datetime.now(tz=timezone.utc).isoformat(),
            "web_search_results": state.web_search_results,
        },
        config,
    )
    response = await llm.ainvoke(message_value, config)
    # We return a list, because this will get added to the existing list
    logger.info(f'response: {response}')
    logger.info(f'retrieved_docs: {state.retrieved_docs}')
    logger.info(f'web_search_results: {state.web_search_results}')
    return {"messages": [response], "retrieved_docs": state.retrieved_docs, "web_search_results": state.web_search_results}
