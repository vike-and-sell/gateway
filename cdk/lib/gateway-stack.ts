import { RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";
import {
  CachePolicy,
  Distribution,
  ResponseHeadersPolicy,
} from "aws-cdk-lib/aws-cloudfront";
import { RestApiOrigin } from "aws-cdk-lib/aws-cloudfront-origins";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export class GatewayStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const api = new RestApi(this, "GatewayRestApi", {
      deploy: true,
    });

    // Account management
    const requestAccountResource = api.root.addResource("request_account");
    requestAccountResource.addMethod("POST", this.handler("request_account"));

    const verifyAccountResource = api.root.addResource("verify_account");
    verifyAccountResource.addMethod("POST", this.handler("verify_account"));

    const requestResetResource = api.root.addResource("request_reset");
    requestResetResource.addMethod("POST", this.handler("request_reset"));

    const verifyResetResource = api.root.addResource("verify_reset");
    verifyResetResource.addMethod("POST", this.handler("verify_reset"));

    const loginResource = api.root.addResource("login");
    loginResource.addMethod("POST", this.handler("login"));

    // Listings
    const listingsResource = api.root.addResource("listings");
    listingsResource.addMethod("GET", this.handler("get_sorted_listings"));
    listingsResource.addMethod("POST", this.handler("create_listing"));

    const listingIdResource = listingsResource.addResource("{listingId}");
    listingIdResource.addMethod("GET", this.handler("get_listing"));
    listingIdResource.addMethod("PATCH", this.handler("update_listing"));
    listingIdResource.addMethod("DELETE", this.handler("delete_listing"));

    const myListingResource = listingsResource.addResource("me");
    myListingResource.addMethod("GET", this.handler("my_listings"));

    // Users
    const usersResource = api.root.addResource("users");

    const userIdResource = usersResource.addResource("{userId}");
    userIdResource.addMethod("GET", this.handler("get_user"));
    userIdResource.addMethod("PATCH", this.handler("update_user"));

    const searchHistoryResource = userIdResource.addResource("searches");
    searchHistoryResource.addMethod("GET", this.handler("get_search_history"));

    const myUserResource = usersResource.addResource("me");
    myUserResource.addMethod("GET", this.handler("my_user"));

    // Ratings & Reviews
    const reviewResource = api.root.addResource("review");
    const reviewIdResource = reviewResource.addResource("{listingId}");
    reviewIdResource.addMethod("GET", this.handler("get_reviews"));
    reviewIdResource.addMethod("POST", this.handler("create_review"));

    const ratingResource = api.root.addResource("rating");
    const ratingIdResource = ratingResource.addResource("{listingId}");
    ratingIdResource.addMethod("GET", this.handler("get_ratings"));
    ratingIdResource.addMethod("POST", this.handler("create_rating"));

    // Search
    const searchResource = api.root.addResource("search");
    searchResource.addMethod("GET", this.handler("search"));

    // Recommendations
    const recommendationsResource = api.root.addResource("recommendations");
    recommendationsResource.addMethod("GET", this.handler("recommendations"));

    const recommendationIdResource =
      recommendationsResource.addResource("{listingId}");
    const ignoreRecommendationByIdResource =
      recommendationIdResource.addResource("ignore");
    ignoreRecommendationByIdResource.addMethod(
      "POST",
      this.handler("ignore_recommendation"),
    );

    // Chats
    const chatsResource = api.root.addResource("chats");
    chatsResource.addMethod("GET", this.handler("chats"));

    const chatIdResource = chatsResource.addResource("{chatId}");
    chatIdResource.addMethod("GET", this.handler("get_chat"));

    const messagesResource = api.root.addResource("messages");
    const messageIdResource = messagesResource.addResource("{chatId}");
    messageIdResource.addMethod("GET", this.handler("get_messages"));

    // Reverse proxy definition using Cloudfront
    const reverseProxy = new Distribution(this, "GatewayReverseProxy", {
      defaultBehavior: {
        origin: new RestApiOrigin(api),
        cachePolicy: CachePolicy.CACHING_DISABLED,
        responseHeadersPolicy:
          ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS_WITH_PREFLIGHT,
      },
    });
  }

  handler(handlerName: string): LambdaIntegration {
    const func = new Function(this, handlerName, {
      runtime: Runtime.PYTHON_3_12,
      code: Code.fromAsset(`packaging/${handlerName}.zip`),
      handler: `${handlerName}.handler`,
    });

    return new LambdaIntegration(func);
  }
}
