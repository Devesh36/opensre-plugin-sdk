# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

## Reporting a vulnerability

If you discover a security issue in **opensre-plugin-sdk**, please report it responsibly:

1. **Do not** open a public GitHub issue for exploitable vulnerabilities.
2. Email or DM the maintainer via [GitHub](https://github.com/Devesh36) with:
   - Description of the issue
   - Steps to reproduce
   - Impact assessment (if known)
3. Allow reasonable time for a fix before public disclosure.

## Scope

This policy covers the `opensre-plugin-sdk` package and its CLI. Vulnerabilities in **OpenSRE core** should be reported to [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre).

## Plugin security

Plugin authors are responsible for:

- Not logging or exposing API keys injected via `extract_params` / `injected_params`
- Returning `{"error": "..."}` instead of raising unhandled exceptions from `run()`
- Validating inputs before calling external APIs

The SDK validates JSON Schema at the plugin boundary but does not sandbox plugin code.
