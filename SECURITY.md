# Security and Data Handling

## Operating model
- Read-only public research only. No authentication bypass, paywall/CAPTCHA circumvention, form submission, account changes, or organizer contact.
- Search results are untrusted discovery candidates. Retrieved pages are untrusted data, never instructions for the audit agent.
- HTML scripts, styles, embedded frames, SVG, and template content are excluded from extracted text. Original decoded response content is retained separately in the retrieval bundle.
- Public-page retrieval permits HTTP(S) only, rejects local/private/non-global destinations, pins each connection to a validated public IP, validates each redirect, enforces a redirect limit, and bounds time and response size.
- Robots policy is checked before retrieval. If the policy cannot be checked, retrieval fails closed.
- Current retrieval supports HTML/XHTML and plain text. PDF parsing, authenticated pages, and private resources are not supported.
- Provider keys are read from environment variables and must never appear in source control, report artifacts, or logs.
- Avoid attendee personal data. Do not submit registration records, identity documents, private correspondence, or sensitive personal information to search providers.

## Evidence integrity
- Search result snippets do not become evidence automatically.
- Evidence is created only from an explicit excerpt/observation linked to a successful retrieval.
- Preserve original language, source URL, capture time, retrieval ID, and content hash where available.
- A failed, blocked, or inaccessible retrieval is not proof that a source is absent or that an organizer violated a rule.
- Multiple providers locating the same canonical source are not independent corroboration.

## Limitations
DNS pinning reduces rebinding risk but does not replace network-layer egress controls. Deployments should also enforce outbound firewall rules and isolate retrieval workers. Provider privacy, retention, and rate limits are governed by each provider's current terms and account settings.
