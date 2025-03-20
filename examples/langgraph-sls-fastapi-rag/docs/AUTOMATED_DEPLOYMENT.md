# Deployment Guide

## Overview

This document provides a comprehensive guide on the automated deployment process utilizing GitHub Actions within our project. The Continuous Deployment (CD) framework facilitates the automatic deployment to distinct environments, ensuring a streamlined and efficient deployment pipeline.

## High-Level Flow

### Production Deployment

1. **Trigger:** Production deployment is initiated either:

   - **Manually:** Through the GitHub Actions tab by selecting the `prod` environment.
   - **Automatically:** By pushing a tag that follows the `v*` pattern.

2. **Workflow Execution:** The Continuous Deployment workflow checks the trigger conditions and proceeds with the production deployment job if criteria are met.

3. **Deployment Execution:** It then invokes the Deployment Workflow with `production` as the target environment. The workflow configures the runner, installs dependencies, sets up AWS credentials, and carries out the deployment to the production environment.

### Staging Deployment

1. **Trigger:** Deployment to `staging` can be initiated in two ways:

   - **Manual Trigger:** Through the GitHub Actions tab by selecting the `staging` environment.
   - **Automatic Trigger:** By pushing to the `main` branch or creating a tag that matches the `staging-v*` pattern.

2. **Workflow Execution:** Upon trigger, the Continuous Deployment workflow evaluates the conditions and identifies the deployment job for the `staging` environment.

3. **Deployment Execution:** The workflow then calls the Deployment Workflow, passing `staging` as the environment to deploy to. This workflow prepares the environment, sets up AWS credentials, and executes the deployment command.

### Development Deployment

1. **Trigger:** Deployment to `dev` is initiated manually through the GitHub Actions tab by selecting the `dev` environment.

2. **Workflow Execution:** The Continuous Deployment workflow identifies the deployment job for the `dev` environment and proceeds with the deployment process.

3. **Deployment Execution:** The Deployment Workflow is called with `dev` as the target environment. It configures the environment, installs dependencies, sets up AWS credentials, and deploys the application.

### Custom Stage Deployment

> NOTE: This is a custom environment that can be defined by the user. For this to work, you need to create a new file in the `sls/envs` directory with the name `config.<stage>.yml` where `<stage>` is the name of the custom stage.

1. **Trigger:** Deployment to a custom environment is initiated manually through the GitHub Actions tab by selecting the `custom` environment.
2. **Workflow Execution:** The Continuous Deployment workflow identifies the deployment job for the `custom` environment and proceeds with the deployment process.
3. **Deployment Execution:** The Deployment Workflow is called with the custom environment as the target. It configures the environment, installs dependencies, sets up AWS credentials, and deploys the application.

## Workflows

### Continuous Deployment

> **File:** `.github/workflows/cd.yml`

This workflow automates the deployment process to specified environments, triggered by manual intervention, push events, or tag creation. It supports deploying to `prod`, `staging`, `dev`, and `custom` environments based on predefined conditions.

#### Triggers

- **Manual Trigger:** Via GitHub Actions with environment selection.
- **Push Event:** To `main` branch, including `staging-v*`, `v*` tags.

#### Jobs

- **Prod:** Targets the production environment upon manual selection or tag creation.
- **Staging:** Targets the staging environment through manual selection, push to `main`, or tag creation.
- **Custom Environment:** Deploys to a user-specified environment upon manual trigger.

### Deployment Workflow

> **File:** `.github/workflows/deployment_call.yml`

Invoked by the Continuous Deployment workflow, it handles the actual deployment process, requiring environment specification and AWS credentials.

#### Inputs

- **Environment:** Deployment target environment.
- **AWS Credentials:** Access key and secret key for AWS deployment.

#### Deployment Jobs

- **Deploy:** Configures the environment, installs dependencies, sets AWS credentials, and deploys the application.

## Deployment Steps

1. **Trigger Selection:** Initiate deployment via manual trigger or automatic conditions.
2. **Environment Determination:** The workflow identifies the target environment based on the trigger.
3. **Execution of Deployment Workflow:** Calls the appropriate deployment job with the specified environment.
4. **Setup and Configuration:** Prepares the deployment environment and configures necessary credentials.
5. **Application Deployment:** Executes deployment to the selected environment.

## Requirements

- GitHub repository with Actions enabled.
- AWS account and credentials.
- Permissions for workflow triggers within the GitHub repository.
