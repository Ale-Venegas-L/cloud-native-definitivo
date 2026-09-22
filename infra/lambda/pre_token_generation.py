import json
import os
import boto3


def lambda_handler(event, context):
    cognito = boto3.client("cognito-idp")

    user_attributes = event["request"]["userAttributes"]
    sub = user_attributes["sub"]
    user_pool_id = event["userPoolId"]

    try:
        user = cognito.admin_get_user(
            UserPoolId=user_pool_id,
            Username=sub,
        )

        custom_attrs = {
            attr["Name"]: attr["Value"]
            for attr in user.get("UserAttributes", [])
            if attr["Name"].startswith("custom:")
        }

        admin_value = custom_attrs.get("custom:admin", "0")
        is_admin = admin_value == "1" or admin_value.lower() == "true"

        permissions = custom_attrs.get("custom:permissions", "")

        event["response"] = {
            "claimsOverrideDetails": {
                "claimsToAddOrOverride": {
                    "custom:admin": str(is_admin).lower(),
                    "custom:permissions": permissions,
                }
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        event["response"] = {"claimsOverrideDetails": {}}

    return event
