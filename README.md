# FurCon Compliance Audit

**Version 2.0.0 · MIT · Platform-neutral core**

Evidence-led preliminary review of convention terms, privacy notices, codes of conduct, registration rules, and event policies. Not legal advice, legal opinion, certification, or guarantee.

## v2
- Platform-neutral domain/application core.
- Capability-based optional adapters.
- Source → Retrieval → Evidence → Claim → Assessment → Finding traceability.
- Separate legal authorities and legal propositions.
- JSON/Markdown canonical outputs; DOCX/HTML/PDF optional.
- Draft 2020-12 domain schemas and semantic reference validation.

## Quick start
Python 3.10+.

~~~bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
furcon-audit examples/sample-report.v1.json --markdown report.md
~~~

Core validation/rendering has no network dependency. Provider adapters are optional and use REST over the Python standard library; no provider is assumed connected.

## Optional web-search providers

The first adapters support Exa and Firecrawl. Add keys to the process environment or your deployment secret manager; never commit keys or paste them into source files.

~~~bash
export EXA_API_KEY="..."
export FIRECRAWL_API_KEY="..."
~~~

~~~python
from furcon_audit.capabilities import CapabilityRegistry
from furcon_audit.providers import ExaAdapter, FirecrawlAdapter

registry = CapabilityRegistry()
registry.register(ExaAdapter())
registry.register(FirecrawlAdapter())
result = registry.execute_with_fallback(
    "search.web", "search", {"query": "official event privacy policy", "limit": 5}
)
~~~

Adapters normalize result metadata and provider request IDs where available. Retries are bounded and limited to transient HTTP/network failures. Fallback is capability-scoped and follows registration order. A missing key marks that adapter unavailable. Search results remain discovery leads—not legal evidence by themselves. Verify original sources, jurisdiction, issuer, status, date, and context before making an assessment.

Legal applicability is fact-specific. Do not infer it solely from attendee nationality or website accessibility. Missing text/search failure does not prove breach. Preserve original-language material and translation provenance. Human review is required for legal conclusions.
