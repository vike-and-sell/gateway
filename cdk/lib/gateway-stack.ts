import { RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class GatewayStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const handler = new Function(this, "test-fn", {
      runtime: Runtime.PYTHON_3_12,
      code: Code.fromAsset("asset.zip"),
      handler: "get_listing_by_id.handler",
    });
  }
}
