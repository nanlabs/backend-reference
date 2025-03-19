#!/bin/bash

# Script to set up SSM parameters for your application
# This uses values from your dev environment configuration

# Set variables
SERVICE_NAME="langgraph-sls-fastapi-rag"  # Replace with your actual service name
STAGE="dev"                       # Using dev stage for the values
SERVICE_STAGE="${SERVICE_NAME}/${STAGE}"
SERVICE_COMMON="${SERVICE_NAME}/common"

echo "Setting up SSM parameters for ${SERVICE_STAGE} and ${SERVICE_COMMON}..."

# Stage-specific parameters
echo "Setting parameters for ${SERVICE_STAGE}/openai-api-key"
echo "Setting parameters for ${SERVICE_STAGE}/openai-api-key"
if [ -z "${OPENAI_API_KEY}" ]; then
    echo "Error: OPENAI_API_KEY is not set"
    exit 1
fi
aws ssm put-parameter --name "/${SERVICE_STAGE}/openai-api-key" \
    --value "${OPENAI_API_KEY}" \
    --type "SecureString" \
    --overwrite

echo "Setting parameters for ${SERVICE_STAGE}/pinecone-api-key"
aws ssm put-parameter --name "/${SERVICE_STAGE}/pinecone-api-key" \
    --value "${PINECONE_API_KEY}" \
    --type "SecureString" \
    --overwrite

echo "Setting parameters for ${SERVICE_STAGE}/pinecone-index-name"
aws ssm put-parameter --name "/${SERVICE_STAGE}/pinecone-index-name" \
    --value "${PINECONE_INDEX_NAME}" \
    --type "String" \
    --overwrite

echo "Setting parameters for ${SERVICE_STAGE}/tavily-api-key"
aws ssm put-parameter --name "/${SERVICE_STAGE}/tavily-api-key" \
    --value "${TAVILY_API_KEY}" \
    --type "SecureString" \
    --overwrite

echo "Setting parameters for ${SERVICE_STAGE}/s3-bucket-name"
aws ssm put-parameter --name "/${SERVICE_STAGE}/s3-bucket-name" \
    --value "${S3_BUCKET_NAME}" \
    --type "String" \
    --overwrite

# Common parameters (shared across stages)
echo "Setting parameters for ${SERVICE_COMMON}/langsmith-api-key"
aws ssm put-parameter --name "/${SERVICE_COMMON}/langsmith-api-key" \
    --value "${LANGCHAIN_API_KEY}" \
    --type "SecureString" \
    --overwrite

echo "Setting parameters for ${SERVICE_COMMON}/langsmith-tracing-v2"
aws ssm put-parameter --name "/${SERVICE_COMMON}/langsmith-tracing-v2" \
    --value "${LANGCHAIN_TRACING_V2}" \
    --type "String" \
    --overwrite

aws ssm put-parameter --name "/${SERVICE_COMMON}/langsmith-callbacks-background" \
    --value "${LANGCHAIN_CALLBACKS_BACKGROUND}" \
    --type "String" \
    --overwrite

echo "SSM parameters setup complete!"