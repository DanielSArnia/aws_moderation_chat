from constructs import Construct
import aws_cdk as core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_cloudfront as cloudfront 
from aws_cdk import aws_cloudfront_origins as origins 
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import Duration
from aws_cdk import aws_dynamodb
import os

class ArniaNicknameModerationAppStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # # S3 Bucket for app data 
        # app_data_bucket = s3.Bucket(self, "arnia-nickname-moderation-storage-backend", versioned=True)
        # Create Cognito User Pool
        # user_pool = cognito.UserPool(self, "UserPool",
        #     sign_in_aliases=cognito.SignInAliases(username=True, email=True),
        #     self_sign_up_enabled=True,
        #     auto_verify=cognito.AutoVerifiedAttrs(email=True)
        # )

        # # Create Cognito User Pool Client
        # user_pool_client = user_pool.add_client("UserPoolClient",
        #     auth_flows=cognito.AuthFlow(user_password=True)
        # )

        # # Create Cognito Authorizer
        # cognito_authorizer = apigateway.CognitoUserPoolsAuthorizer(
        #     self, "CognitoAuthorizer",
        #     cognito_user_pools=[user_pool]
        # )

        nickname_table = aws_dynamodb.Table(
            self, "arnia-nickname-moderation-nickname-table",
            partition_key=aws_dynamodb.Attribute(name="nickname", type=aws_dynamodb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY  # Only for dev!
        )

        # IAM Role for Lambda to access Bedrock
        bedrock_role = iam.Role(self, "arnia-nickname-moderation-bedrock-lamba-role",
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
        bedrock_lambda = _lambda.Function(self, "arnia-nickname-moderation-bedrock-lambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/bedrock"),
            role=bedrock_role,
            timeout=Duration.minutes(3)
            # environment={
            #     # "BUCKET_NAME": app_data_bucket.bucket_name
            # }
        )
        nickname_table.grant_read_write_data(bedrock_lambda)
        bedrock_lambda.add_environment("NICKNAME_TABLE", nickname_table.table_name)

        # API Gateway for Bedrock Lambda function
        bedrock_api = apigateway.RestApi(self, "arnia-nickname-moderation-bedrock-api",
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
        bucket = s3.Bucket(self, "arnia-nickname-moderation-react-app", 
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
        #     self, 'arnia-nickname-moderation-authentication-lambda-edge',
        #     code=_lambda.Code.from_asset('lambda'),
        #     handler='auth_function.handler',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        # )

        # Run a build script with environment variables injected into the build process
        # Use subprocess to trigger the build script
        react_app_path = os.path.join(os.path.dirname(__file__), '..', '..', 'web_app', 'nickname_app')

        # Set environment variables (Bedrock API URL) and run the build command
        os.environ["REACT_APP_BEDROCK_API_URL"] = bedrock_api.url

        # Assuming you have 'npm run build' or 'yarn build' as the build command
        os.system(f"cd {react_app_path} && npm run build")

        # CloudFront Distribution for React app
        distribution = cloudfront.Distribution(self, "arnia-nickname-moderation-react-app-distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    bucket, 
                    origin_access_levels=[cloudfront.AccessLevel.READ, cloudfront.AccessLevel.READ_VERSIONED, cloudfront.AccessLevel.WRITE, cloudfront.AccessLevel.DELETE]
                ),
            ),
            default_root_object='index.html'
        )

        # Deploy the React app to the S3 bucket
        s3_deployment.BucketDeployment(self, "arnia-nickname-moderation-react-app-deploy",
            sources=[s3_deployment.Source.asset(os.path.join(react_app_path, 'dist'))],
            destination_bucket=bucket,
            distribution=distribution,  # Invalidate CloudFront cache on new deploy
            distribution_paths=['/', '/static/*', '/static/css/*', '/static/js/*', '/static/media/*']
        )

        # Output CloudFront URL for React app
        core.CfnOutput(self, "CloudFrontURL", value=distribution.distribution_domain_name)
