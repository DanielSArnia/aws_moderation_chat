from aws_cdk import core
from lib.app_stack import BedrockAppStack

app = core.App()
BedrockAppStack(app, "BedrockAppStack")
app.synth()