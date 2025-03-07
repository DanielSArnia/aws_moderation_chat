import aws_cdk as core
from lib.app_stack import ArniaChatModerationAppStack

app = core.App()
ArniaChatModerationAppStack(app, "ArniaChatModerationStack")
app.synth()