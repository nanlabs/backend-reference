# LocalStack

## Requirements

- [docker](https://www.docker.com/)

## Resources

Once the docker compose is up, it will create the following resources:

- [S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)

You can check the creation of the resources in the `../docker/localstack/` folder.

## Testing

From outside the container you can execute the following commands to test the service each service:

- **S3**

```sh
$ export AWS_ACCESS_KEY_ID=dummy-value
$ export AWS_SECRET_ACCESS_KEY=dummy-value
$ aws --endpoint-url=http://localhost:4566 s3 ls
2022-08-08 03:16:01 example-bucket
```

## LocalStack Desktop

You can use [LocalStack Desktop](https://docs.localstack.cloud/user-guide/tools/localstack-desktop/) to manage the resources created by the docker compose.
