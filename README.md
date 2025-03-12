# Aws Nickname Validation POC

## Overview
This application is designed to **generate** and **validate** nicknames for a **LEGO-based platform**, ensuring they are creative, appropriate, and compliant with global regulations. The system leverages **Large Language Models (LLMs)** to both create and evaluate nicknames while strictly adhering to **COPPA**, **GDPR**, and other relevant data privacy and child protection laws.

![Project Diagram](assets/project_diagram.png)

## Key Features
- 🚀 **Nickname Generation**  
  Uses LLMs to create fun, safe, and engaging nicknames suitable for users of all ages, particularly children.

- 🛡️ **Validation Engine**  
  - Validates **user-submitted nicknames**.  
  - Validates **LLM-generated nicknames**.  
  - Ensures compliance with LEGO’s platform guidelines, including restrictions on language, personal information, and appropriateness.

- ⚖️ **Regulatory Compliance**  
  - Adheres to **COPPA** (Children's Online Privacy Protection Act) regulations to protect children’s privacy.  
  - Complies with **GDPR** (General Data Protection Regulation) standards for data privacy and security.  
  - Filters out any personally identifiable information (PII), offensive language, or inappropriate content.

- ⚙️ **Customizable Ruleset**  
  Validation logic can be adjusted to fit additional platform guidelines or regional compliance requirements.

## Purpose
The goal of this application is to provide a **safe and fun user experience** by ensuring that all nicknames are appropriate for a **child-friendly online environment**, such as LEGO’s digital platforms. By integrating AI-powered generation with robust validation, the system guarantees both creativity and safety.

## Technology Stack

- **Frontend**:  
  - React + Vite  
  - Deployed via **AWS S3** + **CloudFront** for scalable and secure web delivery  
  - User authentication powered by **AWS Cognito**

- **Backend**:  
  - Python (AWS Lambda functions)  
  - Exposed through **AWS API Gateway**  
  - Serverless architecture for efficient and scalable backend processing

- **AI/ML**:  
  - **AWS Bedrock** for scalable LLM-powered nickname generation and validation  
  - Calls to Large Language Models (LLMs) for generating creative, compliant nicknames and performing advanced validation

- **Compliance Framework**:  
  - Custom validation logic enforcing **COPPA**, **GDPR**, and LEGO-specific rules  
  - Filters to ensure no PII, inappropriate language, or rule violations are present in nicknames

- **Infrastructure & Deployment**:  
  - Infrastructure-as-Code (IaC) with AWS CDK 

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
ArniaNicknameModerationBackendStack.userPoolClientId = dnboeaj82649jo3hs028grjl4
ArniaNicknameModerationBackendStack.userPoolId = eu-west-1_Pgq8zS6v3
```

Example of .env file with filled out variables:

```
VITE_BEDROCK_API_URL=https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
VITE_USER_POOL_ID=eu-west-1_Pgq8zS6v3
VITE_USER_POOL_CLIENT_ID=dnboeaj82649jo3hs028grjl4
VITE_AWS_REGION=eu-west-1
```

### 3. Deploying the website

Note: This step requires to have the React + Vite installed

For this final step we need to just run the cdk build for the web.

```bash
cd infrastructure
cdk deploy ArniaNicknameModerationFrontendStack
```
