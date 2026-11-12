from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
)
from aws_cdk import (
    aws_apigateway as apigw,
)
from aws_cdk import (
    aws_lambda as _lambda,
)
from aws_cdk import (
    aws_s3 as s3,
)
from constructs import Construct


class FirewatchPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        # S3 upload bucket deployment.
        upload_bucket = s3.Bucket(
            self,
            "FirewatchUploadBucket",
            cors=[
                s3.CorsRule(
                    allowed_methods=[
                        s3.HttpMethods.GET,
                        s3.HttpMethods.POST,
                        s3.HttpMethods.PUT,
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )
            ],
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="ExpireUploadsAfterOneDay",
                    expiration=Duration.days(1),
                )
            ],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        # Presigned URL generation lambda function.
        generate_url_lambda = _lambda.Function(
            self,
            "GenerateUrlHandler",
            runtime=_lambda.Runtime.PYTHON_3_14,
            # Bundle the root but only include the src directory.
            code=_lambda.Code.from_asset(
                ".",
                exclude=[
                    "*",
                    ".*",
                    ".ruff_cache",
                    ".ruff_cache/**",
                    "!src",
                    "!src/**",
                    "src/**/__pycache__",
                    "src/**/__pycache__/**",
                    "src/**/*.pyc",
                    "src/**/*.pyo",
                ],
            ),
            handler="src.transfer_lambda.generate_url",
            timeout=Duration.seconds(10),
            memory_size=128,
            environment={
                "BUCKET_NAME": upload_bucket.bucket_name,
            },
        )

        # Permission assignment of S3 for generation lambda.
        upload_bucket.grant_put(generate_url_lambda)

        # Quickhull URL generation lambda function.
        quickhull_lambda = _lambda.Function(
            self,
            "QuickhullHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            # Bundle the root but only include the src directory.
            code=_lambda.Code.from_asset(
                ".",
                exclude=[
                    "*",
                    ".*",
                    ".ruff_cache",
                    ".ruff_cache/**",
                    "!src",
                    "!src/**",
                    "src/**/__pycache__",
                    "src/**/__pycache__/**",
                    "src/**/*.pyc",
                    "src/**/*.pyo",
                ],
            ),
            handler="src.quickhull_lambda.lambda_handler",
            timeout=Duration.seconds(30),
            memory_size=1024,
            environment={
                "BUCKET_NAME": upload_bucket.bucket_name,
            },
        )

        # Permission assignment of S3 for quickhull lambda.
        upload_bucket.grant_read_write(quickhull_lambda)

        # API gateway linked to both lambdas.
        api = apigw.RestApi(
            self,
            "FirewatchApi",
            rest_api_name="Firewatch Geospatial Service",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=["GET", "POST", "OPTIONS"],
            ),
        )

        generate_url_resource = api.root.add_resource("generate_url")
        generate_url_resource.add_method(
            "POST", apigw.LambdaIntegration(generate_url_lambda)
        )

        quickhull_resource = api.root.add_resource("quickhull_download")
        quickhull_resource.add_method(
            "POST", apigw.LambdaIntegration(quickhull_lambda)
        )
