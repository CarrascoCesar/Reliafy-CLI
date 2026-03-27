# Authentication

Reliafy CLI requires authentication with the Reliafy API to run analyses, design optimizations, and simulations.

Authentication is provided through [Auth0](https://auth0.com), a widely used identity platform.

!!! info "Automatic authentication"
    You do not need to authenticate manually before using Reliafy CLI. The first time you run any command (`analyze`, `design`, `simulate`, etc.), the CLI automatically checks for a valid token. If none is found, it starts the Auth0 device flow and prompts you to log in before the command proceeds. Subsequent commands reuse the stored token silently.

    You can also trigger or re-run authentication at any time using `reliafy user auth`.

## Authenticate User

Start the authentication flow to obtain an access token:

```bash
reliafy user auth
```

This command initiates the Auth0 device flow:

1. A device code and user code will be displayed
2. You'll be prompted to visit a URL
3. Enter the user code in your browser
4. **First time:** select **Sign up** to create your account. On subsequent logins, select **Log in**
5. Authorize the application
6. Return to the CLI — authentication will complete automatically

The access token is stored securely and used for subsequent API requests.

## Check Authentication Status

Verify your current authentication status and user ID:

```bash
reliafy user id
```

This displays:
- Your authenticated user ID
- Whether you're currently authenticated
- If not authenticated, prompts you to run `reliafy user auth`

## Authentication Notes

- Access tokens expire after a set period - you'll need to re-authenticate when they expire
- The CLI uses Auth0 device flow, which doesn't require storing client secrets
- Authentication credentials are stored locally and not transmitted except to the Reliafy API
- No client secret is used in the CLI - only public Auth0 values (domain, client ID, audience)

## Troubleshooting

If you encounter authentication issues:

- Reliafy includes automatic recovery logic: it checks whether your stored token is still valid, attempts refresh when possible, and falls back to a new Auth0 device login flow when required.

1. Ensure you have an active internet connection
2. Check that you can access the Auth0 authorization URL in your browser
3. Verify your user account has proper permissions
4. Try re-authenticating: `reliafy user auth`

For persistent issues, contact support or check the Reliafy API documentation.
