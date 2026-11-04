# FurCon Compliance Audit

**Version 2.0.0 · MIT · Platform-neutral core**

Evidence-led preliminary review of convention terms, privacy notices, codes of conduct, registration rules, and event policies. Not legal advice, legal opinion, certification, or guarantee.

## v2
- Platform-neutral domain/application core.
- Capability-based optional adapters.
- Source → Retrieval → Evidence → Claim → Assessment → Finding traceability.
- Separate legal authorities and legal propositions.
- JSON/Markdown canonical outputs; DOCX/HTML/PDF optional.
- 15 Draft 2020-12 domain schemas plus semantic reference validation and translation provenance.

## Quick start
Python 3.10+.

~~~bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
furcon-audit examples/sample-report.v1.json --markdown report.md
~~~

Core validation/rendering has no network dependency. Provider adapters are interfaces only; no provider is assumed connected. Agent/provider compatibility remains unverified until conformance tests pass.

Legal applicability is fact-specific. Search snippets are discovery leads only. Missing text does not prove breach. Preserve original-language material and translation provenance.
