#!/bin/sh

if [ -z "${AWS_S3_BUCKET_NAME}" ]; then
	echo "AWS_S3_BUCKET_NAME is not set. Exiting."
	exit 1
fi

# Create S3 bucket
awslocal s3 mb s3://"${AWS_S3_BUCKET_NAME}"
