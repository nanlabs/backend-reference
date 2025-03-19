import logging

import dotenv
import pytest
from langchain_core.runnables import RunnableConfig

from app.index_graph import create_rag_graph
from app.rag_graph import create_graph

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping index graph test")
async def test_index_graph():
    dotenv.load_dotenv('.env.local')
    user_id = "test_user"
    obj = {
        "user_id": user_id,
        "index_name": "test-index",
        "retriever_provider": "pinecone",
        "embedding_model": "openai/text-embedding-3-small",
    }
    # Create the base configuration
    config = RunnableConfig(
        configurable=obj
    )
    graph = create_rag_graph()
    result = await graph.ainvoke({
        "user_id": "test_user",
        "docs": []
    },config=config)
    assert result is not None

@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping rag graph test")
async def test_rag_graph():
    dotenv.load_dotenv('.env.local')
    user_id = "test_user"
    obj = {
        "user_id": user_id,
        "index_name": "test-index",
        "retriever_provider": "pinecone",
        "embedding_model": "openai/text-embedding-3-small",
        "thread_id": "1234567890",
    }
    # Create the base configuration
    config = RunnableConfig(
        configurable=obj
    )
    graph = create_graph()
    result = await graph.ainvoke({
        "user_id": "test_user",
        "queries": ["Give me NAN labs content"],
        "messages": [
            {"role": "user", "content": "Giveme NAN labs"}
        ]
    },config=config)
    assert result is not None