import os

from fastapi import APIRouter
from app.rag_graph import create_graph
from app.router.schemas import RetrieveRequest, RetrieveResponse, StatusResponse, WebSearchResult

router = APIRouter()


@router.get("/", operation_id="get_statuses")
def get_statuses() -> StatusResponse:
    data = ['open', 'in_progress', 'done']
    return StatusResponse(data=data)


@router.post("/", operation_id="retrieve")
async def retrieve(request: RetrieveRequest) -> RetrieveResponse:
    index_name = os.environ["PINECONE_INDEX_NAME"]
    obj = {
            "user_id": request.user_id,
            "index_name": index_name,
            "retriever_provider": "pinecone",
            "embedding_model": "openai/text-embedding-3-small",
            "thread_id": request.thread_id,
            "aws_region": "us-west-2"
        }
    # Create the base configuration
    graph = create_graph()

    result = await graph.ainvoke({
        "messages": request.messages,
        "user_id": request.user_id
    }, obj)
    
    # Convert web search results to the correct format
    web_search_results = [
        WebSearchResult(
            title=item.get('title', ''),
            url=item.get('url', ''),
            content=item.get('content', ''),
            score=item.get('score', 0.0)
        ) 
        for item in result['web_search_results']
    ]
    
    return RetrieveResponse(
        messages=result['messages'], 
        retrieved_docs=result['retrieved_docs'], 
        web_search_results=web_search_results
    )