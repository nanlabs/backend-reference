from fastapi import APIRouter
import os
from app.index_graph import create_graph
from app.router.schemas import IndexRequest, StatusResponse

router = APIRouter()


@router.get("/", operation_id="get_statuses")
def get_statuses() -> StatusResponse:
    data = ['open', 'in_progress', 'done']
    return StatusResponse(data=data)


@router.post("/", operation_id="run_index")
@router.post("/", operation_id="run_index")
async def run_index(request: IndexRequest) -> StatusResponse:
    try:
        # Validate user_id
        if not request.user_id or not isinstance(request.user_id, str):
            raise ValueError("Invalid user_id")
 
        # Get environment variables safely
        index_name = os.environ.get("PINECONE_INDEX_NAME")
        if not index_name:
            raise ValueError("PINECONE_INDEX_NAME environment variable is not set")
 
        obj = {
            "user_id": request.user_id,
            "index_name": index_name,
            "retriever_provider": "pinecone",
            "embedding_model": "openai/text-embedding-3-small",
        }
        # Create the base configuration
        graph = create_graph()
 
        result = await graph.ainvoke({"user_id": request.user_id, "docs": None}, obj)
        
        # Verify result contains necessary data
        if "docs" not in result:
            return StatusResponse(data=[], error="No documents found")
            
        return StatusResponse(data=result['docs'])
    except Exception as e:
        # Log the error
        import logging
        logging.error(f"Error in run_index: {str(e)}")
        return StatusResponse(data=[], error=str(e))
    
    return StatusResponse(data=result['docs'])