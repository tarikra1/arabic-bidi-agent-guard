# Security Policy

## Hidden Bidirectional Unicode Mitigation (`CVE-2021-42574`)

Invisible Unicode bidirectional control characters (`U+200E`, `U+200F`, `U+202A`–`U+202E`, `U+2066`–`U+2069`) can visually reorder tokens in source code and documentation ("Trojan Source" attacks).

`arabic-bidi-agent-guard` detects all hidden directional control characters under rule `HIDDEN_BIDI_CONTROLS` and strips them cleanly via:

```bash
bidi-guard strip-controls <path>
```

## Reporting a Vulnerability

Please report security issues privately through GitHub Security Advisories on [tarikra1/arabic-bidi-agent-guard](https://github.com/tarikra1/arabic-bidi-agent-guard/security) rather than opening a public issue with exploit payloads.
