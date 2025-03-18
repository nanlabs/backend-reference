"""This "graph" simply exposes an endpoint for a user to upload docs to be indexed."""


from langgraph.graph import StateGraph

from app.index_graph import configuration, nodes, state



def create_rag_graph():
    """Create and return the index graph."""
    # Define a new graph
    builder = StateGraph(state.IndexState, config_schema=configuration.IndexConfiguration)
    builder.add_node(nodes.fetch_s3_content)
    builder.add_node(nodes.index_docs)
    builder.add_edge("__start__", "fetch_s3_content")
    builder.add_edge("fetch_s3_content", "index_docs")
    builder.add_edge("index_docs", "__end__")
    # This compiles it into a graph you can invoke and deploy.
    graph = builder.compile()
    graph.name = "S3IndexGraph"
    return graph

