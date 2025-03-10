import aws_cdk as core
from lib.backend_stack import ArniaNicknameModerationBackendStack
from lib.frontend_stack import ArniaNicknameModerationFrontendStack
import os

react_app_path = os.path.join(os.path.dirname(__file__), '..', '..', 'web_app', 'nickname_app')
app = core.App()

# Deploy the backend stack first
backend_stack = ArniaNicknameModerationBackendStack(app, "ArniaNicknameModerationBackendStack")

# Deploy the frontend stack and pass the backend API URL
frontend_stack = ArniaNicknameModerationFrontendStack(app, "ArniaNicknameModerationFrontendStack", react_app_path=react_app_path)


app.synth()