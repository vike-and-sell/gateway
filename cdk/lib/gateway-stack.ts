import { Stack, StackProps } from "aws-cdk-lib";
import { Code, Function, LayerVersion, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import { PythonLayerVersion } from "@aws-cdk/aws-lambda-python-alpha";
import { DomainName, HttpApi, HttpMethod } from "aws-cdk-lib/aws-apigatewayv2";
import { HttpLambdaIntegration } from "aws-cdk-lib/aws-apigatewayv2-integrations";
import { ARecord, HostedZone, RecordTarget } from "aws-cdk-lib/aws-route53";
import { ApiGatewayv2DomainProperties } from "aws-cdk-lib/aws-route53-targets";
import { Certificate } from "aws-cdk-lib/aws-certificatemanager";

export class GatewayStack extends Stack {
  readonly layer: LayerVersion;
  readonly api: HttpApi;
  readonly domain: DomainName | undefined;

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const domainName = "vas.brnn.ca";
    let zone;
    try {
      zone = HostedZone.fromLookup(this, "BrnnHostedZone", {
        domainName: "brnn.ca",
      });

      if (zone) {
        const cert = Certificate.fromCertificateArn(
          this,
          `BrnnCert`,
          "arn:aws:acm:us-east-1:446708209687:certificate/fcbd7810-fab9-48a4-8f07-e0545199abec",
        );
        this.domain = new DomainName(this, "BrnnDomain", {
          domainName,
          certificate: cert,
        });
        new ARecord(this, "BrnnARecord", {
          recordName: domainName,
          zone,
          target: RecordTarget.fromAlias(
            new ApiGatewayv2DomainProperties(
              this.domain.regionalDomainName,
              this.domain.regionalHostedZoneId,
            ),
          ),
        });
      }
    } catch {}

    this.layer = new PythonLayerVersion(this, "PythonLayerFromRequirements", {
      layerVersionName: "gateway-python-layer",
      entry: "packaging/layer",
      compatibleRuntimes: [Runtime.PYTHON_3_12],
    });

    this.api = new HttpApi(this, "GatewayHttpApi", {
      corsPreflight: {
        allowOrigins: ["*"],
      },
      defaultDomainMapping: this.domain
        ? {
            domainName: this.domain,
          }
        : undefined,
    });

    // Account management
    this.route(HttpMethod.POST, "/request_account", "request_account");

    this.route(HttpMethod.POST, "/verify_account", "verify_account");

    this.route(HttpMethod.POST, "/request_reset", "request_reset");

    this.route(HttpMethod.POST, "/verify_reset", "verify_reset");

    this.route(HttpMethod.POST, "/login", "login");

    // Listings

    this.route(HttpMethod.GET, "/listings", "get_sorted_listings");
    this.route(HttpMethod.POST, "/listings", "create_listing");

    this.route(HttpMethod.GET, "/listings/{listingId}", "get_listing");
    this.route(HttpMethod.PATCH, "/listings/{listingId}", "update_listing");
    this.route(HttpMethod.DELETE, "/listings/{listingId}", "delete_listing");

    this.route(HttpMethod.GET, "/listings/me", "my_listings");

    // Users
    this.route(HttpMethod.GET, "/users/{userId}", "get_user");
    this.route(HttpMethod.PATCH, "/users/{userId}", "update_user");

    this.route(
      HttpMethod.GET,
      "/users/{userId}/searches",
      "get_search_history",
    );

    this.route(HttpMethod.GET, "/users/me", "my_user");

    // Ratings & Reviews
    this.route(HttpMethod.GET, "/reviews/{listingId}", "get_reviews");
    this.route(HttpMethod.POST, "/reviews/{listingId}", "create_review");

    this.route(HttpMethod.GET, "/ratings/{listingId}", "get_ratings");
    this.route(HttpMethod.POST, "/ratings/{listingId}", "create_rating");

    // Search
    this.route(HttpMethod.GET, "/search", "search");

    // Recommendations
    this.route(HttpMethod.GET, "/recommendations", "recommendations");

    this.route(
      HttpMethod.POST,
      "/recommendations/{listingId}/ignore",
      "ignore_recommendation",
    );

    // Chats
    this.route(HttpMethod.GET, "/chats", "chats");
    this.route(HttpMethod.POST, "/chats", "create_chat");

    this.route(HttpMethod.GET, "/chats/{chatId}", "get_chat");

    this.route(HttpMethod.GET, "/messages/{chatId}", "get_messages");
    this.route(HttpMethod.POST, "/messages/{chatId}", "create_message");
  }

  handler(handlerName: string): HttpLambdaIntegration {
    const func = new Function(this, handlerName, {
      runtime: Runtime.PYTHON_3_12,
      code: Code.fromAsset(`packaging/${handlerName}.zip`),
      handler: `${handlerName}.handler`,
      layers: [this.layer],
      environment: {
        DATA_URL: process.env.DATA_URL ?? "",
        DATA_API_KEY: process.env.DATA_API_KEY ?? "",
        JWT_SECRET_KEY: process.env.JWT_SECRET_KEY ?? "",
        MAPS_API_KEY: process.env.MAPS_API_KEY ?? "",
        SMTP_SERVER: process.env.SMTP_SERVER ?? "",
        SMTP_PORT: process.env.SMTP_PORT ?? "",
        SMTP_USERNAME: process.env.SMTP_USERNAME ?? "",
        SMTP_PASSWORD: process.env.SMTP_PASSWORD ?? "",
      },
    });

    return new HttpLambdaIntegration(`${handlerName}-integration`, func);
  }

  route(method: HttpMethod, path: string, name: string) {
    this.api.addRoutes({
      path,
      methods: [method],
      integration: this.handler(name),
    });
  }
}
