# Testing checklist — hardening fork

Use this when students implement fixes in a **private fork** (never in the public vulnerable tree).

## Authorization

- [ ] Every tool that accepts resource IDs checks tenant + ownership.
- [ ] Negative tests: user A cannot access user B objects.

## Tool surface

- [ ] High-impact tools removed from default allowlists.
- [ ] Tool descriptions reviewed for imperative language.

## Logging

- [ ] Each tool invocation emits structured audit with args hash.
- [ ] Logs redact secrets and model-visible tokens.

## Web UI

- [ ] No `innerHTML` with model/tool output without sanitization.
- [ ] CSP deployed on the lab SPA if you extend the UI.

## Configuration

- [ ] Debug endpoints disabled outside explicit maintenance mode.
- [ ] CORS restricted to known origins.
- [ ] Rate limits on scenario endpoints if exposed beyond localhost.

## Supply chain

- [ ] Lockfile + hash pinning for MCP SDK and server dependencies.
- [ ] CI step verifying tool manifest matches signed release artifact.
