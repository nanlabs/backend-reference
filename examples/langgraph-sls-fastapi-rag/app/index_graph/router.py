from fastapi import APIRouter
import os
from app.index_graph import create_rag_graph
from app.router.schemas import IndexRequest, StatusResponse

router = APIRouter()


@router.get("/", operation_id="get_statuses")
def get_statuses() -> StatusResponse:
    data = ['open', 'in_progress', 'done']
    return StatusResponse(data=data)


@router.post("/", operation_id="run_index")
async def run_index(request: IndexRequest) -> StatusResponse:

    index_name = os.environ["PINECONE_INDEX_NAME"]
    obj = {
            "user_id": request.user_id,
            "index_name": index_name,
            "retriever_provider": "pinecone",
            "embedding_model": "openai/text-embedding-3-small",
        }
    # Create the base configuration
    graph = create_rag_graph()

    result = await graph.ainvoke({"user_id": request.user_id, "docs": None }, obj)
    
    return StatusResponse(data=result['docs'])