# Phase 2C.2 — Dedicated Security Review

**Status:** Security hardening implemented; final CI/static-scan verification pending.  
**Scope:** URL parsing, SSRF controls, DNS resolution and pinning, redirects, robots policy, retrieval resource limits, provider transport, API query boundaries, and static dependency/code scanning.

## Findings and fixes

| ID | Area | Severity | Finding | Disposition |
|---|---|---:|---|---|
| 2C2-01 | URL parsing | High | Invalid ports and malformed URL inputs could raise raw parsing exceptions instead of controlled policy errors. | Fixed: URL type, empty values, control characters, malformed ports, and non-standard ports are rejected as blocked retrieval targets. |
| 2C2-02 | Port policy | Medium | HTTP and HTTPS could use the other scheme's standard port. | Fixed: only port 80 for HTTP and 443 for HTTPS are accepted. |
| 2C2-03 | Redirect downgrade | High | HTTPS-to-HTTP redirects could be followed before final response validation. | Fixed: redirect targets are validated before connection; HTTPS downgrade is blocked. |
| 2C2-04 | Custom retrieval boundary | Medium | A malformed custom fetch response could cause attribute/type errors instead of a controlled retrieval result. | Fixed: response status, headers, body, and final URL types are validated. |
| 2C2-05 | Resource exhaustion | High | Callers could request arbitrarily large retrieval limits or timeouts. | Fixed: retrieval body limit is capped at 10 MB and timeout at 60 seconds; booleans and invalid numeric types are rejected. |
| 2C2-06 | Robots policy | Medium | A malformed or oversized robots response was not explicitly validated at the policy boundary. | Fixed: response shape is validated and robots content is capped at 2 MB; failures remain fail-closed. |
| 2C2-07 | Provider credential forwarding | High | Default urllib redirect behavior could potentially forward custom provider authentication headers to a redirect destination. | Fixed: provider transport uses a no-redirect handler. Redirect responses are treated as HTTP errors; credentials are not forwarded to a new host. |
| 2C2-08 | Provider input abuse | Medium | Search query length, retry count, and provider timeout were not all bounded. | Fixed: query length capped at 4,000 characters, retries at five, and timeout at 60 seconds; malformed payloads are rejected. |
| 2C2-09 | Provider response contract | Medium | Transport status/header shape checks needed to reject malformed responses consistently. | Fixed: response status, headers, and body are validated before parsing or metadata extraction. |
| 2C2-10 | Static security scan | Low | Bandit flagged an assert in a provider error path. | Fixed: replaced with an explicit ProviderError branch. Re-run pending. |

## Existing controls reviewed

- HTTP and HTTPS only.
- Rejects local hostnames and non-global IP addresses.
- Resolves and checks all DNS answers before retrieval.
- Pins each connection to a validated IP address.
- Re-resolves and validates each redirect destination before connecting.
- Redirect count is limited.
- TLS certificate validation and hostname SNI are retained for HTTPS.
- Robots policy is checked before page retrieval; policy lookup failures fail closed.
- Retrieval response bodies are read with a byte ceiling.
- HTML extraction excludes script, style, iframe, SVG, template, and noscript contents.
- Provider responses are bounded to 2 MB.
- Provider keys are sourced from environment variables and are not logged by the adapter.
- Search candidates remain untrusted leads and do not automatically become evidence or claims.

## Automated security checks

The dedicated CI security job now runs:
- pip-audit against the project dependency set.
- Bandit against the Python source tree.

An earlier dependency scan reported no known vulnerabilities. The first Bandit run found one low-severity assert-use issue, which was corrected. The final clean scan must be confirmed by the latest workflow run before this phase is marked fully green.

## Residual risks and verification limits

- DNS pinning and public-IP checks are application-layer controls, not a substitute for outbound firewall policy, isolated retrieval workers, or network egress restrictions.
- No live hostile-network SSRF test was performed in this review.
- No live Exa or Firecrawl API requests were made.
- Provider terms, data retention, and external service behavior remain subject to their current policies.
- No external penetration test or independent security review has been completed.
- Retrieved content remains untrusted. This core does not provide an LLM sandbox or guarantee prompt-injection immunity.

## Recommendation

Treat this phase as code-level security hardening, not a security certification. Confirm the final Python matrix and security-static job, then proceed to a dedicated integration/conformance phase and independent review before any stable release.
