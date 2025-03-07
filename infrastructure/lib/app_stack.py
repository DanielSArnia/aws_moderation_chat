import aws_cdk as core
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_s3_deployment as s3_deployment
import os

class BedrockAppStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 Bucket for app data 
        app_data_bucket = s3.Bucket(self, "arnia-chat-moderation-storage-backend", versioned=True)

        # IAM Role for Lambda to access Bedrock
        bedrock_role = iam.Role(self, "arnia-chat-moderation-bedrock-lamba-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # Attach permission to invoke Bedrock model
        bedrock_role.add_to_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]  # Restrict this to specific models if possible
        ))

        # Lambda Function to interact with Bedrock
        lambda_function = lambda_.Function(self, "arnia-chat-moderation-bedrock-lambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("lambda"),  # Assume code is in 'lambda' directory
            role=bedrock_role,
            environment={
                "BUCKET_NAME": app_data_bucket.bucket_name
            }
        )

        # API Gateway for Bedrock Lambda function
        api = apigateway.LambdaRestApi(self, "arnia-chat-moderation-bedrock-lambda-api",
            handler=lambda_function,
            proxy=True
        )

        # Output API Gateway URL for the Lambda function
        core.CfnOutput(self, "ApiEndpoint", value=api.url)
        # TODO: This api-url has to be sent to the web build
        # Probably building the react app here is required

        # S3 Bucket for React app hosting
        bucket = s3.Bucket(self, "arnia-chat-moderation-react-app", 
            versioned=True,
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            enforce_ssl=True,
            website_index_document="index.html",
            website_error_document="index.html",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # CloudFront Distribution for React app
        distribution = cloudfront.CloudFrontWebDistribution(self, "arnia-chat-moderation-react-app-distribution",
            origin_configs=[{
                's3_origin_source': cloudfront.S3OriginConfig(
                    s3_bucket_source=bucket
                ),
                'behaviors': [{'is_default_behavior': True}],
            }]
        )

        # Deploy the React app to the S3 bucket
        s3_deployment.BucketDeployment(self, "arnia-chat-moderation-react-app-deploy",
            sources=[s3_deployment.Source.asset(os.path.join(os.path.dirname(__file__), '..', '..', 'web_app', 'chat_app', 'build'))],
            destination_bucket=bucket,
            distribution=distribution,  # Invalidate CloudFront cache on new deploy
            distribution_paths=['/', '/static/*', '/static/css/*', '/static/js/*', '/static/media/*']
        )

        # Output CloudFront URL for React app
        core.CfnOutput(self, "CloudFrontURL", value=distribution.distribution_domain_name)
