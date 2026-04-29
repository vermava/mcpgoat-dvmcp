# Pseudo detection ideas (not production rules)

These are **teaching stubs**. Tune heavily before any real SIEM deployment.

## High-impact tool followed by rapid retrieval

```yaml
title: MCP export after broad retrieval (pseudo)
logsource:
  category: application
  product: mcp-lab-example
detection:
  selection_export:
    tool_name: export_all_user_data
  selection_read:
    tool_name: build_context_from_docs
  condition: selection_read followed_by selection_export within 5m
```

## Shadow tool usage

```yaml
title: Shadow MCP tool invocation
detection:
  tool_name: shadow_mcp_ping
```

## Verbose error leak pattern

```yaml
title: HTTP 500 includes traceback field
detection:
  status: 500
  field_exists: traceback
```
