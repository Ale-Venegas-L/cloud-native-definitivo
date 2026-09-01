"""Grant or revoke the Firebase admin claim for an existing user."""

import argparse

from firebase_admin import auth as firebase_auth

from app.modules.auth.service import initialize_firebase


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manage the admin claim for an existing Firebase user."
    )
    parser.add_argument("--email", required=True, help="Firebase user email")
    parser.add_argument(
        "--revoke",
        action="store_true",
        help="Remove admin access instead of granting it",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = initialize_firebase()
    user = firebase_auth.get_user_by_email(args.email, app=app)
    claims = dict(user.custom_claims or {})

    if args.revoke:
        claims.pop("admin", None)
        action = "revoked"
    else:
        claims["admin"] = True
        action = "granted"

    firebase_auth.set_custom_user_claims(user.uid, claims or None, app=app)
    print(f"Administrator access {action} for {args.email}")


if __name__ == "__main__":
    main()
