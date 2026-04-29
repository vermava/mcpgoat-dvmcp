# Worksheet answer key (instructor)

> Do not distribute this file to students as part of the vulnerable app bundle in classroom setups where answers should stay private.

## Lab 01

1. `list_documents`
2. `export_all_user_data`
3. User-controlled channels are untrusted; treating them as instructions collapses policy boundaries for tool routing.
4. Example answers: human-in-the-loop for exports, allowlisted tools per workflow, instruction/data separation.

## Lab 02

1. Accept any imperative phrase copied from the tool description (for example “PRIORITY: Call this tool first…”).
2. It triggers `compliance_pre_check` which dispatches to an export-style payload (`export_all_user_data` path).
3. Expect answers about manifest review, signed releases, pinning hashes, and restricting unknown tools.

## Lab 03

1. `read`, `rename`, `delete`, `export` (as implemented).
2. Violates least privilege; expands blast radius for a single compromised decision.
3. Expect separate tools or separate capability tokens per action.

## Lab 04

1. `secrets` array / `get_server_env_snapshot` output.
2. Example: `logger.warning` including export reasons near `export_all_user_data`.
3. Short-lived scoped tokens, vault references, or no secret material in model-visible channels.

## Lab 05

1. Bob (user id 2).
2. `get_document` should enforce `owner_user_id == ctx.user_id` (plus tenant checks in multi-tenant systems).
3. Example: `test_get_document_forbidden_for_other_owner`.

## Lab 06

1. `documents` id `3` body contains an HTML comment with hidden instructions.
2. HTML comments still reach plain-text concatenation paths and can steer models.
3. Strip comments, normalize whitespace, chunk with provenance, block unknown ingest sources.

## Lab 07

1. No — simulation only.
2. `template` parameter to `run_report_generator`.
3. Structured fields (report type enum, validated parameters) instead of a single free-form template string.

## Lab 08

1. `innerHTML` on `#unsafe-sink`.
2. Client-side assignment bypasses server-side HTML escaping for that DOM subtree.
3. CSP, sanitization library (if HTML required), using text nodes / framework escaping.

## Lab 09

1. No — counts should remain flat in the vulnerable build.
2. Example fields: `timestamp`, `actor_id`, `tool_name`, `args_sha256`, `outcome`, `latency_ms`, `session_id`.
3. Sequence analytics: read sensitive doc → export; unusual tool frequency; missing audit when policy requires it.

## Lab 10

1. Example: `debug_mode=True`, `cors_allow_all=True`, `expose_stack_traces=True`.
2. Represents unapproved / shadow connector surface enabled by default.
3. Secure-by-default profile with explicit env toggles for diagnostics; deny shadow tools in prod manifests.
