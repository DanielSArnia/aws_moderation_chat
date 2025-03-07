# Aws Moderation Chat POC test

## Prerequirements

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