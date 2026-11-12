import aws_cdk as cdk
from firewatch_stack import FirewatchPipelineStack

app = cdk.App()

FirewatchPipelineStack(
    app,
    "FirewatchPipelineStack",
    env=cdk.Environment(region="eu-north-1"),
)

app.synth()
