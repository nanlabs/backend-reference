import logging
import os
from typing import Optional

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig

from app.index_graph.retrieval import make_retriever
from app.index_graph.services import S3CSVReader
from app.index_graph.state import IndexState

logger = logging.getLogger(__name__)

async def index_docs(
    state: IndexState, *, config: Optional[RunnableConfig] = None
) -> IndexState:
    """Index the documents in the state."""
    if not config:
        raise ValueError("Configuration required to run index_docs.")

    try:
        with make_retriever(config) as retriever:
            logger.info(f"Starting document indexing process with {len(state.docs)} documents")
            await retriever.aadd_documents(state.docs)
        logger.info("Document indexing process completed successfully")
        return state
    except Exception as e:
        logger.error(f"Failed to index documents: {str(e)}")
        raise


async def fetch_s3_content(
    state: IndexState,
    config: Optional[RunnableConfig] = None,
) -> dict[str, str]:
    """Fetch content from S3."""

    bucket_name = os.environ["S3_BUCKET_NAME"]
    service = S3CSVReader(
        bucket_name,
        prefix="/"
    )
    logger.info(f"Fetching content from S3 bucket '{bucket_name}'")
    file_contents = service.read_all_csv_files()
    base_metadata = {
        "source": "s3"
    }
    docs = [Document(page_content=row['content'], metadata={ **base_metadata, 'title': row['title'], 'created_at': row['created']}) for row in file_contents]
    logger.info(f"Successfully processed {len(docs)} S3 documents")
    return {"docs": docs}
