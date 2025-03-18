"""Main entrypoint for the conversational retrieval graph.

This module defines the core structure and functionality of the conversational
retrieval graph. It includes the main graph definition, state management,
and key functions for processing user inputs, generating queries, retrieving
relevant documents, and formulating responses.
"""

import os

from langgraph.graph import StateGraph
from langgraph_checkpoint_dynamodb import DynamoDBSaver
from langgraph_checkpoint_dynamodb.config import DynamoDBConfig, DynamoDBTableConfig

from app.rag_graph.configuration import Configuration
from app.rag_graph.nodes import create_query, respond, retrieve, web_search
from app.rag_graph.state import State


def create_checkpointer():
    """Factory function to create a DynamoDB checkpointer singleton."""
    checkpoints_table_name = os.environ.get('CHECKPOINT_TABLE_NAME')
    config = DynamoDBConfig(
        table_config=DynamoDBTableConfig(
            table_name=checkpoints_table_name,
        ),
    )
    return DynamoDBSaver(config=config)

def create_graph():
    builder = StateGraph(State, input=State, config_schema=Configuration)

    builder.add_node(retrieve)
    builder.add_node(web_search)
    builder.add_node(respond)
    builder.add_node(create_query)
    builder.add_edge("__start__", "create_query")
    builder.add_edge("create_query", "retrieve")
    builder.add_edge("retrieve", "web_search")
    builder.add_edge("web_search", "respond")
    builder.add_edge("respond", "__end__")

    # Use the factory to create the checkpointer
    checkpointer = create_checkpointer()

    #print the graph image
    graph = builder.compile(
        checkpointer=checkpointer,
        interrupt_before=[],  # if you want to update the state before calling the tools
        interrupt_after=[],
    )
    graph.name = "RetrievalGraph"
    return graph


# Call the create_graph function to initialize the graph
