# Serverless Deployment

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)

We use Serverless Framework to do production ready deployments.

## Requirements

**You’ll need to have Node 18 or later on your local development machine** (but it’s not required on the server). You can use [fnm](https://github.com/Schniz/fnm) to easily switch Node versions between different projects.

```sh
fnm use
pnpm install
```

## AWS Lambda Deployment

To deploy the app to AWS, you'll first need to configure your AWS credentials. There are many ways
to set your credentials, for more information refer to the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

Once set you can deploy your app using the serverless framework with:

```sh
pnpm run sls:deploy --stage <stage>
```

for example, to deploy to the `staging` stage:

```sh
pnpm run sls:deploy --stage staging
```
