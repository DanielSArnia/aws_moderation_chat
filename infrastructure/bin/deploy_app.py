import aws_cdk as core
from lib.app_stack import ArniaNicknameModerationAppStack

app = core.App()
ArniaNicknameModerationAppStack(app, "ArniaNicknameModerationStack")
app.synth()