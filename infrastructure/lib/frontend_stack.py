from constructs import Construct
import aws_cdk as core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront as cloudfront 
from aws_cdk import aws_cloudfront_origins as origins 
from aws_cdk import aws_s3_deployment as s3_deployment
import os

class ArniaNicknameModerationFrontendStack(core.Stack):
    def __init__(self, scope: Construct, id: str, react_app_path:str, **kwargs):
        super().__init__(scope, id, **kwargs)

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