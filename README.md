# FurCon Compliance Audit

**Version 2.0.0 (unreleased source version) · MIT · Platform-neutral core**

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

Adapters normalize result metadata and provider request IDs where available. Retries are bounded and limited to transient HTTP/network failures. Fallback is capability-scoped and follows registration order. A missing key marks that adapter unavailable. Search results remain discovery leads—not legal evidence by themselves.

## Public-page retrieval

Phase 2B.2 adds a separate retrieval layer. It accepts one candidate URL and produces a normalized Source record, a timestamped Retrieval record, and a content bundle containing the original decoded response separately from extracted text. The response is represented by a SHA-256 content hash; the full body is not silently promoted into Evidence.

~~~python
from furcon_audit.retrieval import retrieve_page

capture = retrieve_page("https://example.org/event/terms")
if capture["retrieval"]["outcome"] == "success":
    text = capture["content"]["extracted_text"]
    content_hash = capture["retrieval"]["content_hash"]
~~~

Retrieval is read-only, HTTP(S)-only, public-network-only, robots-aware, and size/time bounded. Local/private targets, restricted responses, robots disallowances, and unsupported media types are recorded as blocked retrievals—not treated as proof that a source does not exist. The current adapter supports HTML/XHTML and plain text; PDF and authenticated content are intentionally out of scope. Network behavior is tested with mocks; live retrieval is opt-in.

## Legal methodology

Legal applicability is fact-specific. Do not infer it solely from attendee nationality or website accessibility. Missing text/search failure does not prove breach. Preserve original-language material and translation provenance. Human review is required for legal conclusions. See `IMPLEMENTATION_ROADMAP.md` for phases 2B.1–2B.10.


## Security and conformance

See [SECURITY.md](SECURITY.md) for retrieval and data-handling boundaries and [COMPATIBILITY.md](COMPATIBILITY.md) for verified versus unverified integrations. Exa/Firecrawl tests use mocked REST fixtures; they are not live-provider certifications or agent-runtime compatibility claims.

## Search-to-retrieval orchestration

The core can now connect a configured search registry to the public-page retrieval layer without creating Evidence automatically:

~~~python
from furcon_audit.pipeline import run_research_task
from furcon_audit.research import ResearchTask

task = ResearchTask(
    "task_policy_001", "audit_001", "Find official event policies",
    ("identify official policy sources",),
)
result = run_research_task(task, registry, "official event privacy and refund policy")
~~~

The result preserves task/attempt records, source identities, retrieval records, captured content, and unresolved gaps. Evidence and claims remain empty until explicitly created through the evidence/claim workflow.
