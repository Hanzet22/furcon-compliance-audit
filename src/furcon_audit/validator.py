"""Schema and cross-reference validation for canonical audit reports."""
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
    """Validate references defensively, including when called without schema validation."""
    if not isinstance(report, dict):
        return ["$: report must be an object"]
    errors, indexes = [], {}
    keys = {
        "research_tasks":"research_task_id", "research_attempts":"attempt_id",
        "sources":"source_id", "retrievals":"retrieval_id", "evidence":"evidence_id",
        "claims":"claim_id", "legal_authorities":"authority_id",
        "legal_propositions":"proposition_id", "jurisdiction_assessments":"jurisdiction_assessment_id",
        "assessments":"assessment_id", "findings":"finding_id", "human_reviews":"review_id",
        "translations":"translation_id"
    }
    for collection, key in keys.items():
        rows = report.get(collection, [])
        if not isinstance(rows, list):
            errors.append(f"{collection}: expected an array")
            indexes[collection] = {}
            continue
        index = {}
        for pos, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"{collection}[{pos}]: expected an object")
                continue
            value = row.get(key)
            if not isinstance(value, str) or not value:
                errors.append(f"{collection}[{pos}].{key}: missing ID")
            elif value in index:
                errors.append(f"{collection}: duplicate ID {value}")
            else:
                index[value] = row
        indexes[collection] = index

    def check_refs(source, field, target):
        rows = report.get(source, [])
        if not isinstance(rows, list):
            return
        for pos, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            values = row.get(field, [])
            if values is None: values = []
            if isinstance(values, str): values = [values]
            if not isinstance(values, list):
                errors.append(f"{source}[{pos}].{field}: expected an ID or array of IDs")
                continue
            for ref in values:
                if not isinstance(ref, str) or ref not in indexes[target]:
                    errors.append(f"{source}[{pos}].{field}: unresolved {target} ID {ref}")

    relations = [
        ("research_attempts","research_task_id","research_tasks"), ("retrievals","source_id","sources"),
        ("retrievals","attempt_id","research_attempts"), ("evidence","retrieval_id","retrievals"),
        ("claims","evidence_ids","evidence"), ("legal_authorities","retrieval_id","retrievals"),
        ("legal_propositions","authority_ids","legal_authorities"),
        ("jurisdiction_assessments","legal_proposition_ids","legal_propositions"),
        ("assessments","claim_ids","claims"), ("assessments","evidence_ids","evidence"),
        ("assessments","legal_proposition_ids","legal_propositions"),
        ("findings","assessment_ids","assessments"),
        ("findings","jurisdiction_assessment_ids","jurisdiction_assessments"),
        ("findings","supporting_evidence_ids","evidence"), ("findings","contrary_evidence_ids","evidence"),
        ("translations","evidence_id","evidence")
    ]
    for relation in relations: check_refs(*relation)

    known_ids = {row_id for index in indexes.values() for row_id in index}
    reviews = report.get("human_reviews", [])
    if isinstance(reviews, list):
        for pos, review in enumerate(reviews):
            if not isinstance(review, dict): continue
            targets = review.get("target_ids", [])
            if not isinstance(targets, list):
                errors.append(f"human_reviews[{pos}].target_ids: expected an array")
                continue
            for target_id in targets:
                if not isinstance(target_id, str) or target_id not in known_ids:
                    errors.append(f"human_reviews[{pos}].target_ids: unresolved target ID {target_id}")

    findings = report.get("findings", [])
    if isinstance(findings, list):
        for pos, finding in enumerate(findings):
            if not isinstance(finding, dict): continue
            if finding.get("assessment_status") == "supported_concern":
                if not finding.get("supporting_evidence_ids"):
                    errors.append(f"findings[{pos}]: supported concern requires evidence")
                if not finding.get("assessment_ids"):
                    errors.append(f"findings[{pos}]: supported concern requires assessment")
    jurisdictions = report.get("jurisdiction_assessments", [])
    if isinstance(jurisdictions, list):
        for pos, item in enumerate(jurisdictions):
            if isinstance(item, dict) and isinstance(item.get("applicability_status"), str) and item.get("applicability_status") in {"applicable_supported","not_applicable_supported"} and not item.get("legal_proposition_ids"):
                errors.append(f"jurisdiction_assessments[{pos}]: supported applicability requires legal propositions")
    tasks = report.get("research_tasks", [])
    if isinstance(tasks, list):
        for pos, task in enumerate(tasks):
            if isinstance(task, dict) and task.get("status") in {"partial","blocked","failed"} and not task.get("blocked_reason"):
                errors.append(f"research_tasks[{pos}]: status requires blocked_reason")
    return errors

def validate_report(report):
    """Schema validation gates semantic checks to avoid unsafe assumptions on malformed data."""
    schema_errors = validate_schema(report)
    return schema_errors if schema_errors else validate_report_semantics(report)
