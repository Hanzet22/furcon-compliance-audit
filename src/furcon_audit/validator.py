import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"

def validate_schema(data, schema_name="report.schema.json"):
    schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{'/'.join(map(str, error.absolute_path)) or '$'}: {error.message}" for error in validator.iter_errors(data)]

def validate_report_semantics(report):
    errors, indexes = [], {}
    keys = {
        "research_tasks":"research_task_id", "research_attempts":"attempt_id",
        "sources":"source_id", "retrievals":"retrieval_id", "evidence":"evidence_id",
        "claims":"claim_id", "legal_authorities":"authority_id",
        "legal_propositions":"proposition_id", "jurisdiction_assessments":"jurisdiction_assessment_id",
        "assessments":"assessment_id", "findings":"finding_id", "human_reviews":"review_id"
    }
    for collection, key in keys.items():
        index = {}
        for pos, row in enumerate(report.get(collection, [])):
            value = row.get(key)
            if not isinstance(value, str):
                errors.append(f"{collection}[{pos}].{key}: missing ID")
            elif value in index:
                errors.append(f"{collection}: duplicate ID {value}")
            else:
                index[value] = row
        indexes[collection] = index

    def check_refs(source, field, target):
        for pos, row in enumerate(report.get(source, [])):
            values = row.get(field, []) or []
            if isinstance(values, str):
                values = [values]
            for ref in values:
                if ref not in indexes[target]:
                    errors.append(f"{source}[{pos}].{field}: unresolved {target} ID {ref}")

    relations = [
        ("research_attempts","research_task_id","research_tasks"),
        ("retrievals","source_id","sources"), ("retrievals","attempt_id","research_attempts"), ("evidence","retrieval_id","retrievals"),
        ("claims","evidence_ids","evidence"), ("legal_authorities","retrieval_id","retrievals"), ("legal_propositions","authority_ids","legal_authorities"),
        ("jurisdiction_assessments","legal_proposition_ids","legal_propositions"),
        ("assessments","claim_ids","claims"), ("assessments","evidence_ids","evidence"),
        ("assessments","legal_proposition_ids","legal_propositions"),
        ("findings","assessment_ids","assessments"),
        ("findings","jurisdiction_assessment_ids","jurisdiction_assessments"),
        ("findings","supporting_evidence_ids","evidence"),
        ("findings","contrary_evidence_ids","evidence"), ("translations","evidence_id","evidence")
    ]
    for relation in relations:
        check_refs(*relation)

    for pos, review in enumerate(report.get("human_reviews", [])):\n        valid_targets = set().union(*(set(index.values()) for index in indexes.values()))\n        known_ids = {row_id for index in indexes.values() for row_id in index}\n        for target_id in review.get("target_ids", []):\n            if target_id not in known_ids:\n                errors.append(f"human_reviews[{pos}].target_ids: unresolved target ID {target_id}")\n\n    for pos, finding in enumerate(report.get("findings", [])):
        if finding.get("assessment_status") == "supported_concern":
            if not finding.get("supporting_evidence_ids"):
                errors.append(f"findings[{pos}]: supported concern requires evidence")
            if not finding.get("assessment_ids"):
                errors.append(f"findings[{pos}]: supported concern requires assessment")
    for pos, item in enumerate(report.get("jurisdiction_assessments", [])):
        if item.get("applicability_status") in {"applicable_supported","not_applicable_supported"} and not item.get("legal_proposition_ids"):
            errors.append(f"jurisdiction_assessments[{pos}]: supported applicability requires legal propositions")
    for pos, task in enumerate(report.get("research_tasks", [])):
        if task.get("status") in {"partial","blocked","failed"} and not task.get("blocked_reason"):
            errors.append(f"research_tasks[{pos}]: status requires blocked_reason")
    return errors

def validate_report(report):
    return validate_schema(report) + validate_report_semantics(report)
