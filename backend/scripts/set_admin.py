"""Grant or revoke admin access for a Cognito user via custom attributes.

Usage:
    python scripts/set_admin.py --email user@example.com
    python scripts/set_admin.py --email user@example.com --revoke

Note: Requires a Pre Token Generation Lambda to include custom:admin
in the JWT. See docs/aws-setup.md for configuration.
"""

import argparse
import os

import boto3


def get_cognito_client():
    return boto3.client(
        "cognito-idp",
        region_name=os.getenv("COGNITO_REGION", "us-east-1"),
    )


def get_user_pool_id() -> str:
    pool_id = os.getenv("COGNITO_USER_POOL_ID")
    if not pool_id:
        raise RuntimeError("COGNITO_USER_POOL_ID environment variable not set")
    return pool_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manage admin access for a Cognito user."
    )
    parser.add_argument("--email", required=True, help="Cognito user email")
    parser.add_argument(
        "--revoke",
        action="store_true",
        help="Remove admin access instead of granting it",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = get_cognito_client()
    user_pool_id = get_user_pool_id()

    # Find user by email
    response = client.admin_get_user(
        UserPoolId=user_pool_id,
        Username=args.email,
    )

    # Get current custom attributes
    current_attrs = {
        attr["Name"]: attr["Value"]
        for attr in response.get("UserAttributes", [])
        if attr["Name"].startswith("custom:")
    }

    if args.revoke:
        new_value = "false"
        action = "revoked"
    else:
        new_value = "true"
        action = "granted"

    client.admin_update_user_attributes(
        UserPoolId=user_pool_id,
        Username=args.email,
        UserAttributes=[
            {"Name": "custom:admin", "Value": new_value},
        ],
    )
    print(f"Administrator access {action} for {args.email}")


if __name__ == "__main__":
    main()
