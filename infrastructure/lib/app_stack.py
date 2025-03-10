from constructs import Construct
import aws_cdk as core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_apigatewayv2_integrations
from aws_cdk import aws_apigatewayv2
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_cloudfront as cloudfront 
from aws_cdk import aws_cloudfront_origins as origins 
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_dynamodb
import os

class ArniaChatModerationAppStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # # S3 Bucket for app data 
        # app_data_bucket = s3.Bucket(self, "arnia-chat-moderation-storage-backend", versioned=True)

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
        bedrock_lambda = _lambda.Function(self, "arnia-chat-moderation-bedrock-lambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/bedrock"),
            role=bedrock_role,
            # environment={
            #     # "BUCKET_NAME": app_data_bucket.bucket_name
            # }
        )

        # API Gateway for Bedrock Lambda function
        bedrock_api = apigateway.RestApi(self, "arnia-chat-moderation-bedrock-api",
            rest_api_name="BedrockService",
            description="API to trigger Bedrock Lambda"
        )

        # Define a resource and method for invoking the Lambda
        bedrock_resource = bedrock_api.root.add_resource("check-nickname")
        bedrock_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(
                bedrock_lambda,
                proxy=True,
                integration_responses=[
                    apigateway.IntegrationResponse(
                        status_code="200",
                        response_parameters={
                            "method.response.header.Access-Control-Allow-Origin": "'*'",
                            "method.response.header.Access-Control-Allow-Headers": "'Content-Type'",
                            "method.response.header.Access-Control-Allow-Methods": "'POST'"
                        }
                    )
                ]
            ),
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True
                    }
                )
            ]
        )

        # OPTIONS Method (Preflight)
        bedrock_resource.add_method(
            "OPTIONS",
            apigateway.MockIntegration(
                integration_responses=[apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": "'Content-Type'",
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                        "method.response.header.Access-Control-Allow-Methods": "'OPTIONS,POST'"
                    }
                )],
                passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                request_templates={
                    "application/json": "{\"statusCode\": 200}"
                }
            ),
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Methods": True
                    }
                )
            ]
        )

        # # Output API Gateway URL for the Lambda function
        core.CfnOutput(self, "BedrockApi", value=bedrock_api.url)

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

        # # Lambda function (must be in us-east-1 for Lambda@Edge)
        # auth_lambda = _lambda.Function(
        #     self, 'arnia-chat-moderation-authentication-lambda-edge',
        #     code=_lambda.Code.from_asset('lambda'),
        #     handler='auth_function.handler',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        # )

        # CloudFront Distribution for React app
        distribution = cloudfront.Distribution(self, "arnia-chat-moderation-react-app-distribution-test",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    bucket, 
                    origin_access_levels=[cloudfront.AccessLevel.READ, cloudfront.AccessLevel.READ_VERSIONED, cloudfront.AccessLevel.WRITE, cloudfront.AccessLevel.DELETE]
                ),
            ),
            default_root_object='index.html'
        )

        # Deploy the React app to the S3 bucket
        s3_deployment.BucketDeployment(self, "arnia-chat-moderation-react-app-deploy-test",
            sources=[s3_deployment.Source.asset(os.path.join(os.path.dirname(__file__), '..', '..', 'web_app', 'chat_app', 'dist'))],
            destination_bucket=bucket,
            distribution=distribution,  # Invalidate CloudFront cache on new deploy
            distribution_paths=['/', '/static/*', '/static/css/*', '/static/js/*', '/static/media/*']
        )

        # Output CloudFront URL for React app
        core.CfnOutput(self, "CloudFrontURL", value=distribution.distribution_domain_name)
