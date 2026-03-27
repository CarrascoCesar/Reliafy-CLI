"""
auth_cli.py
This module handles authentication for the Reliafy CLI using Auth0's Device Authorization Flow.
Copyright (c) 2025 Cesar Carrasco. All rights reserved.
"""

import json
import os
import time
import webbrowser
from pathlib import Path

import jwt
import requests
from platformdirs import user_config_dir
from rich.console import Console

from reliafy.utils.icons import ICON_ERR, ICON_INFO, ICON_LINK, ICON_LOGIN, ICON_OK, ICON_WARN
from reliafy.utils.utilities import safe_write_json

console = Console()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "auth.reliafy.app")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "V3SC7HrE6Auw40Rn2iiMqAJayM3wQg7P")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "https://reliafy.up.railway.app")

APP_NAME = "Reliafy"
TOKEN_FILE = Path(user_config_dir(APP_NAME)) / "auth_tokens.json"


def save_tokens(data: dict) -> None:
    try:
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise Exception(f"{ICON_ERR} Failed to create token file directory {TOKEN_FILE.parent.name}: {e}")

    try:
        safe_write_json(data, TOKEN_FILE, indent=2)
    except Exception as e:
        raise Exception(f"{ICON_ERR} Failed to write token file {TOKEN_FILE.name}: {e}")

    try:
        TOKEN_FILE.chmod(0o600)
    except Exception:
        pass  # ignore errors


def load_tokens() -> dict | None:
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            console.print(f"{ICON_WARN} Warning: failed to parse token file {TOKEN_FILE.name}: {e}")
            return None
        except Exception as e:
            console.print(f"{ICON_WARN} Warning: failed to read token file {TOKEN_FILE.name}: {e}")
            return None
    return None


def is_token_valid(token_data: dict) -> bool:
    if not token_data:
        return False

    expires_at = token_data.get("expires_at")
    if expires_at is None:
        console.print(f"{ICON_WARN} Token missing expiration time, treating as expired")
        return False

    # Add 5-minute buffer before expiration
    return time.time() < (expires_at - 300)


def refresh_access_token(old_tokens: dict) -> dict:
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": old_tokens["refresh_token"],
    }
    try:
        # Auth0 expects application/x-www-form-urlencoded for /oauth/token
        response = requests.post(url, data=payload, timeout=15)
        # Attempt to parse JSON regardless of status for better error messages
        try:
            resp_json = response.json()
        except ValueError:
            resp_json = None
        if response.status_code != 200:
            # Provide more precise error context than a generic network error
            err = None
            desc = None
            if isinstance(resp_json, dict):
                err = resp_json.get("error")
                desc = resp_json.get("error_description")
            msg = f"HTTP {response.status_code}"
            if err:
                msg += f" - {err}"
            if desc:
                msg += f": {desc}"
            raise Exception(f"{ICON_ERR} Refresh token failed: {msg}")
        # Status 200 OK
        try:
            new_tokens = resp_json if isinstance(resp_json, dict) else response.json()
        except ValueError as e:
            raise Exception(f"{ICON_ERR} Failed to parse refresh response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"{ICON_ERR} Network error refreshing token: {e}")

    # Preserve refresh_token if not rotated
    new_tokens.setdefault("refresh_token", old_tokens["refresh_token"])

    # Preserve id_token if not included
    if "id_token" not in new_tokens and "id_token" in old_tokens:
        new_tokens["id_token"] = old_tokens["id_token"]

    new_tokens["expires_at"] = time.time() + new_tokens["expires_in"]

    save_tokens(new_tokens)
    return new_tokens


def device_login_flow() -> dict | None:
    console.print(f"{ICON_LOGIN} Starting new login flow...")

    url = f"https://{AUTH0_DOMAIN}/oauth/device/code"
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "scope": "openid profile email offline_access",
        "audience": AUTH0_AUDIENCE,
    }

    # Request device code with basic network & JSON handling
    try:
        resp = requests.post(url, data=payload, timeout=15)
        resp.raise_for_status()
        try:
            device_data = resp.json()
        except ValueError as e:
            console.print(f"{ICON_ERR} Failed to parse Auth0 response: {e}")
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"{ICON_ERR} Network error requesting device code: {e}")
        return None

    # Validate required fields and open verification link
    link = device_data.get("verification_uri_complete") or device_data.get("verification_uri")
    if not link:
        console.print(f"{ICON_ERR} Missing verification link in response.")
        return None
    console.print(f"{ICON_LINK} Going to: [bold blue]{link}[/bold blue] to authorize this device.")
    webbrowser.open(link)

    # Start polling
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    device_code = device_data.get("device_code")
    if not device_code:
        console.print(f"{ICON_ERR} Missing device_code in response.")
        return None
    poll_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code,
        "client_id": AUTH0_CLIENT_ID,
    }

    deadline = time.time() + device_data.get("expires_in", 300)
    interval = device_data.get("interval", 5)
    if not isinstance(interval, (int, float)) or interval <= 0:
        interval = 5

    try:
        while True:
            if time.time() >= deadline:
                console.print(f"{ICON_ERR} Device code expired. Restart login.")
                return None

            time.sleep(interval)
            try:
                resp = requests.post(token_url, data=poll_payload, timeout=15)
            except requests.exceptions.RequestException as e:
                console.print(f"{ICON_ERR} Network error during login: {e}")
                return None

            if resp.status_code == 200:
                try:
                    tokens = resp.json()
                except ValueError as e:
                    console.print(f"{ICON_ERR} Failed to parse token response: {e}")
                    return None
                tokens["expires_at"] = time.time() + tokens["expires_in"]
                save_tokens(tokens)
                console.print(f"{ICON_OK} Login successful!")
                return tokens

            # Safe error extraction for expected non-200 polling responses
            try:
                err = resp.json().get("error")
            except ValueError:
                console.print(f"{ICON_ERR} Unexpected response: {resp.text}")
                return None

            if err == "authorization_pending":
                continue
            if err == "slow_down":
                interval = min(interval + 5, 30)
                continue
            if err == "expired_token":
                console.print(f"{ICON_ERR} Device code expired. Restart login.")
                return None
            if err == "access_denied":
                console.print(f"{ICON_ERR} Access denied by user.")
                return None

            console.print(f"{ICON_ERR} Error during device login: {err}")
            return None
    except KeyboardInterrupt:
        console.print(f"{ICON_WARN} Login canceled by user.")
        return None


def get_user_id() -> str | None:
    """
    Display-only helper: decode 'id_token' without signature verification.
    Returns 'sub' for user reference.
    """
    try:
        tokens = load_tokens()
        token = tokens.get("id_token") if tokens else None
        if not token:
            console.print(f"{ICON_ERR} No ID token found.")
            return None

        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("sub")
    except Exception as e:
        console.print(f"{ICON_ERR} Failed to decode token: {e}")
        return None


def get_token() -> str | None:
    """Return a valid access token, refreshing or running device flow when needed."""
    tokens = load_tokens()

    # Existing, valid token
    if tokens and is_token_valid(tokens):
        return tokens.get("access_token")

    # Try refresh
    if tokens and tokens.get("refresh_token"):
        console.print(f"{ICON_INFO} Refreshing access token...")
        try:
            tokens = refresh_access_token(tokens)
        except Exception as e:
            console.print(f"{ICON_ERR} Error refreshing access token: {e}")
            tokens = None

        if tokens and tokens.get("access_token"):
            return tokens.get("access_token")

    # Otherwise, run device login
    tokens = device_login_flow()
    if not tokens:
        return None

    return tokens.get("access_token")


# auth_cli.py
