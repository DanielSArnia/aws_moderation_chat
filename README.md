# Aws Nickname Validation POC

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Purpose](#purpose)
4. [Technology Stack](#technology-stack)
5. [Prerequisites](#prerequisites)
6. [Deploying the Application](#deploying-the-application)

## Overview
This application is designed to **generate** and **validate** nicknames for a **LEGO-based platform**, ensuring they are creative, appropriate, and compliant with global regulations. The system leverages **Large Language Models (LLMs)** to both create and evaluate nicknames while strictly adhering to **COPPA**, **GDPR**, and other relevant data privacy and child protection laws.

![Project Diagram](assets/project_diagram.png)

## Key Features
- **Nickname Generation**  
  Uses LLMs to create fun, safe, and engaging nicknames suitable for users of all ages, particularly children.

- **Validation Engine**  
  - Validates **user-submitted nicknames**.  
  - Validates **LLM-generated nicknames**.  
  - Ensures compliance with LEGO’s platform guidelines, including restrictions on language, personal information, and appropriateness.

- **Regulatory Compliance**  
  - Adheres to **COPPA** (Children's Online Privacy Protection Act) regulations to protect children’s privacy.  
  - Complies with **GDPR** (General Data Protection Regulation) standards for data privacy and security.  
  - Filters out any personally identifiable information (PII), offensive language, or inappropriate content.

- **Customizable Ruleset**  
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

## Prerequisites

### AWS CLI and CDK

First, install both the AWS CLI and AWS CDK:

#### Installing AWS CLI

You can install AWS CLI manually by downloading and unzipping the installation file:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

#### Installing AWS CDK

AWS CDK is installed using npm as a global package:

Make sure you have npm installed: [Installing nodejs](#installing-nodejs-and-packages)

```bash
npm install -g aws-cdk
```

#### Configuring AWS CLI

Once the AWS CLI is installed, configure the security credentials. The AWS CDK will inherit these credentials from the AWS CLI.

For instructions on setting up the AWS CLI, refer to the [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

To configure the AWS CLI, run:

```bash
aws configure
```

Then, provide your credentials. It is recommended to use short-term credentials with IAM Identity Center for enhanced security.

#### My Setup

For reference, my setup includes the following versions:

- `cdk --version` output: `cdk==2.1003.0 (build b242c23)`
- `aws --version` output: `aws-cli/2.24.19 Python/3.12.9 Linux/6.8.0-52-generic exe/x86_64.ubuntu.22`

### Frontend: React + Vite

For the frontend, you will need **React** and **Vite**.

#### Installing Node.js and Packages

To set up the frontend, follow these steps:

1. **Install Node.js**:  
   You need Node.js to run React and Vite. You can install the latest version of Node.js from [the official Node.js website](https://nodejs.org/), or use a package manager like `nvm` (Node Version Manager) to manage versions.

   - To install `nvm` (optional, but recommended), run the following command in your terminal:  
     `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash`  
     After installation, restart your terminal and then install the latest version of Node.js by running:  
     `nvm install node`

   - Alternatively, you can install Node.js directly from the official website.

2. **Navigate to the Frontend Folder**:  
   Change your directory to the `nickname-app` folder inside the `web` directory:  
   `cd web/nickname-app`

3. **Install Dependencies**:  
   Install the necessary packages, including React and Vite, by running:  
   `npm install`

   This command will install the dependencies listed in the `package.json` file.

4. **Check that everything is set up properly**:  
   After the installation is complete, check the project is bulding:  
   `npm run build`

#### Additional Notes

- Make sure you have the required versions of Node.js and npm for compatibility with React and Vite.
- If you encounter any issues with dependencies or installation, try deleting the `node_modules` folder and the `package-lock.json` file, and then run `npm install` again.

## Deploying the Application

This section outlines the steps required to deploy both the **backend** and **frontend** components of the application.

---

### Overview of Deployment Steps

1. **Set up the Python environment** for the backend.
2. **Deploy the Backend** using AWS CDK.
3. **Configure Environment Variables** using the output from the backend deployment.
4. **Deploy the Frontend** to AWS S3 + CloudFront.

---

## 1. Set up the Python Environment

Before deploying the backend, you need to set up a Python environment using Conda. Follow these steps:

### Installing Conda

If you don't have Conda installed, you can follow these steps to install it:

1. **Download and install Miniconda** (a minimal Conda installer):
   - Go to the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html).
   - Download the appropriate version for your system (e.g., Miniconda3 for Linux, macOS, or Windows).
   - Follow the instructions on the page to install Miniconda.

2. **Verify Conda installation**:  
   After installation, open your terminal and verify that Conda is installed by running:  
   `conda --version`

   This should return the version of Conda you have installed.

### Setting up the Python environment

Once Conda is installed, follow these steps to set up the Python environment:

```bash
conda create -n infrastructure python=3.12
conda activate infrastructure
cd ./infrastructure
pip install -r requirements.txt
```

## 2. Deploying the Backend

Run the following commands to deploy the backend infrastructure:

```bash
cd infrastructure
cdk deploy ArniaNicknameModerationBackendStack
```

**Important**:
Once the deployment is complete, save the output values, as they will be needed in the next step to configure the frontend.

Example CDK Output:

```
Outputs:
ArniaNicknameModerationBackendStack.BedrockApi = https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
ArniaNicknameModerationBackendStack.arnianicknamemoderationbedrockapiEndpoint17D97578 = https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
ArniaNicknameModerationBackendStack.userPoolClientId = dnboeaj82649jo3hs028grjl4
ArniaNicknameModerationBackendStack.userPoolId = eu-west-1_Pgq8zS6v3
```

## 3. Configuring Environment Variables for the Web App

After deploying the backend, you need to configure the frontend environment variables using the outputs from the previous step.

Edit the .env file located at:

```bash
web_app/nickname_app/.env
```

Example .env file:

```dotenv
VITE_BEDROCK_API_URL=https://m8aenb09e8.execute-api.eu-west-1.amazonaws.com/prod/
VITE_USER_POOL_ID=eu-west-1_Pgq8zS6v3
VITE_USER_POOL_CLIENT_ID=dnboeaj82649jo3hs028grjl4
VITE_AWS_REGION=eu-west-1
```

Make sure to replace the values with your actual outputs from Step 1.

## 4. Deploying the Frontend

**Note**:
Ensure you have React and Vite installed in your local environment before proceeding with the build and deployment.

Run the following command to deploy the frontend stack:

```bash
cd infrastructure
cdk deploy ArniaNicknameModerationFrontendStack
```

After deployment, your website will be hosted on AWS S3 and served through CloudFront. The CloudFront URL will be provided as part of the CDK output.

## Deployment Complete

Your application is now fully deployed and ready to use!

If you encounter any issues:

- Verify the `.env` variables are correctly set in the frontend.
- Check the AWS CloudFormation console for the status of your stacks.
- Review the CDK deployment logs for any errors.
