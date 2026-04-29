# Lab 08 — Insecure output handling

## Learning objective

Observe **HTML/script sink** behavior when the browser assigns tool-derived HTML to `innerHTML`.

## OWASP mapping

- **MCP:** MCP10 Context Injection & Over-Sharing (data path into UI)
- **LLM:** LLM05 Improper Output Handling

## Vulnerable behavior

The API returns `unsafe_html_fragment` for Lab 8. The lab page writes it into the DOM without sanitization.

**Code:** `main.py` (`/api/run` branch), `web_ui/templates/lab.html`.

## Student exercise

1. Run with the default snippet containing a harmless `<img … onerror=…>` pattern.
2. In browser devtools, confirm whether the handler executed (modern browsers may still mitigate some cases — discuss why you must not rely on that).

## Expected observation

The vulnerable sink area updates with raw HTML from the tool path.

## Defensive checklist

- Treat model and tool output as untrusted data; encode for the correct context (HTML, JS, URL, CSS).
- Use CSP and structured templating instead of `innerHTML` for dynamic content.
