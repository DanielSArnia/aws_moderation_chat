# Aws Moderation Chat POC test

## Prerequirements

### AWS CLI and CDK:

Install both AWS CLI and AWS CDK:

AWS CLI is installed manually from a zip file:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

AWS CDK we use npm global package installing

```bash
npm install -g aws-cdk
```

We also have to configure the security credentials for AWS CLI (AWS CDK will inherit the credentials of the AWS CLI)

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

To setup AWS CLI you have to run aws configure and then provide your credentials which we recommend you use short term credentials with IAM Identity Center

My setup has the following:
```
cdk==2.1003.0 (build b242c23)
aws-cli==2.24.19
python==3.12.9
```

### For web we will need React + vite

TODO: complete here

## Deploying the applications

This step is very important and it entails the following steps

1. Run the cdk deployment for the backend side of the application

2. Set any variables required by the output of the previous step into the .env of the web app

3. Deploy the frontend side (the website)

### 1. Deploying the backend

Run the following commands to deploy the backend:

Before we do this, make sure you see the output of the deploy, we need to take some variables and place then in the .env in the following step

```bash
cd infrastructure
cdk deploy ArniaNicknameModerationBackendStack
```

### 2. Setting .env variables for web

You have to take the corresponding URL variables and fill all the .env variables that can be found at `web_app/nickname_app/.env`

Given the following outputs:

```
Outputs:
ArniaNicknameModerationBackendStack.BedrockApi = https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
ArniaNicknameModerationBackendStack.arnianicknamemoderationbedrockapiEndpoint17D97578 = https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
```

Example of .env file with filled out variables:

```
VITE_BEDROCK_API_URL=https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
```

### 3. Deploying the website

Note: This step requires to have the React + Vite installed

For this final step we need to just run the cdk build for the web.

```bash
cd infrastructure
cdk deploy ArniaNicknameModerationFrontendStack
```
