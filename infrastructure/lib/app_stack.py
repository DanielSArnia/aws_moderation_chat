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

        ################################ WEBSOCKET APP ##########################################
        # connections_table = aws_dynamodb.Table(
        #     self, "arnia-chat-moderation-connections-table",
        #     partition_key=aws_dynamodb.Attribute(name="connectionId", type=aws_dynamodb.AttributeType.STRING),
        #     removal_policy=core.RemovalPolicy.DESTROY  # Only for dev!
        # )

        # connect_handler = _lambda.Function(
        #     self, "arnia-chat-moderation-connect-handler",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     handler="handler.handler",
        #     code=_lambda.Code.from_asset("lambda/websocket_connect")
        # )

        # disconnect_handler = _lambda.Function(
        #     self, "arnia-chat-moderation-disconnect-handler",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     handler="handler.handler",
        #     code=_lambda.Code.from_asset("lambda/websocket_disconnect")
        # )

        # message_handler = _lambda.Function(
        #     self, "arnia-chat-moderation-message-handler",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     handler="handler.handler",
        #     code=_lambda.Code.from_asset("lambda/websocket_message")
        # )

        # # connect_integration = aws_apigatewayv2.CfnIntegration(
        # #     self, "ConnectIntegration",
        # #     api_id=web_socket_api.ref,
        # #     integration_type="AWS_PROXY",
        # #     integration_uri=f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{connect_handler.function_arn}/invocations"
        # # )

        # # disconnect_integration = aws_apigatewayv2.CfnIntegration(
        # #     self, "DisconnectIntegration",
        # #     api_id=web_socket_api.ref,
        # #     integration_type="AWS_PROXY",
        # #     integration_uri=f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{disconnect_handler.function_arn}/invocations"
        # # )
        # # message_integration = aws_apigatewayv2.CfnIntegration(
        # #     self, "SendMessageIntegration",
        # #     api_id=web_socket_api.ref,
        # #     integration_type="AWS_PROXY",
        # #     integration_uri=f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{message_handler.function_arn}/invocations"
        # # )

        # # connect_route = aws_apigatewayv2.CfnRoute(
        # #     self, "ConnectRoute",
        # #     api_id=web_socket_api.ref,
        # #     route_key="$connect",
        # #     authorization_type="NONE",  # Optional: You can add custom auth later
        # #     target=f"integrations/{connect_integration.ref}"
        # # )

        # # disconnect_route = aws_apigatewayv2.CfnRoute(
        # #     self, "DisconnectRoute",
        # #     api_id=web_socket_api.ref,
        # #     route_key="$disconnect",
        # #     authorization_type="NONE",
        # #     target=f"integrations/{disconnect_integration.ref}"
        # # )
        # # message_route = aws_apigatewayv2.CfnRoute(
        # #     self, "SendMessageRoute",
        # #     api_id=web_socket_api.ref,
        # #     route_key="sendMessage",  # action in client message: { "action": "sendMessage", ... }
        # #     authorization_type="NONE",
        # #     target=f"integrations/{message_integration.ref}"
        # # )

        # # Grant permissions to Lambdas
        # connections_table.grant_read_write_data(connect_handler)
        # connections_table.grant_read_write_data(disconnect_handler)
        # connections_table.grant_read_write_data(message_handler)

        # web_socket_api = aws_apigatewayv2.WebSocketApi(
        #     self,
        #     "arnia-chat-moderation-web-socket",
        #     route_selection_expression="$request.body.action"
        # )
        # # web_socket_api = apigwv2.CfnApi(
        # #     self, "MyWebSocketApi",
        # #     name="mywsapi",
        # #     protocol_type="WEBSOCKET",
        # #     route_selection_expression="$request.body.action"
        # # )
        # # aws_apigatewayv2.WebSocketStage(self, "mystage",
        # #     web_socket_api=web_socket_api,
        # #     stage_name="dev",
        # #     auto_deploy=True
        # # )

        # # connect_handler.add_permission(
        # #     "arnia-chat-moderation-web-socket-invoke-connect",
        # #     principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
        # #     source_arn=f"arn:aws:execute-api:{self.region}:{self.account}:{web_socket_api.ref}/*"
        # # )

        # # disconnect_handler.add_permission(
        # #     "arnia-chat-moderation-web-socket-invoke-disconnect",
        # #     principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
        # #     source_arn=f"arn:aws:execute-api:{self.region}:{self.account}:{web_socket_api.ref}/*"
        # # )

        # # message_handler.add_permission(
        # #     "arnia-chat-moderation-web-socket-invoke-message",
        # #     principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
        # #     source_arn=f"arn:aws:execute-api:{self.region}:{self.account}:{web_socket_api.ref}/*"
        # # )

        # web_socket_api.add_route(
        #     route_key="sendMessage",
        #     integration=aws_apigatewayv2_integrations.WebSocketLambdaIntegration(
        #         "arnia-chat-moderation-message-integration", message_handler
        #     )
        # )

        # web_socket_api.add_route(
        #     route_key="$connect",
        #     integration=aws_apigatewayv2_integrations.WebSocketLambdaIntegration(
        #         "arnia-chat-moderation-connect-integration", connect_handler
        #     )
        # )

        # web_socket_api.add_route(
        #     route_key="$disconnect",
        #     integration=aws_apigatewayv2_integrations.WebSocketLambdaIntegration(
        #         "arnia-chat-moderation-disconnect-integration", disconnect_handler
        #     )
        # )
        # # # 4️⃣ Deployment and Stage (Deploy the API)
        # # deployment = aws_apigatewayv2.CfnDeployment(
        # #     self, "WebSocketApiDeployment",
        # #     api_id=web_socket_api.ref
        # # )

        # # stage = aws_apigatewayv2.CfnStage(
        # #     self, "WebSocketApiStage",
        # #     api_id=web_socket_api.ref,
        # #     deployment_id=deployment.ref,
        # #     stage_name="dev",
        # #     auto_deploy=True
        # # )
        # stage = aws_apigatewayv2.WebSocketStage(
        #     self, "arnia-chat-moderation-web-socket-stage",
        #     web_socket_api=web_socket_api,
        #     stage_name="dev",
        #     auto_deploy=True
        # )

        # # Add environment variable so the lambdas know the table name
        # connect_handler.add_environment("CONNECTION_TABLE", connections_table.table_name)
        # disconnect_handler.add_environment("CONNECTION_TABLE", connections_table.table_name)
        # message_handler.add_environment("CONNECTION_TABLE", connections_table.table_name)
        # message_handler.add_environment("WEBSOCKET_API_ENDPOINT", f"https://{web_socket_api.api_endpoint}/dev")


        # core.CfnOutput(self, "WebSocketApiEndpoint", value=web_socket_api.api_endpoint)

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
