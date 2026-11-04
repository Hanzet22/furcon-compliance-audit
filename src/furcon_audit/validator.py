import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"

def validate_schema(data, schema_name="report.schema.json"):
    schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{'/'.join(map(str,e.absolute_path)) or '$'}: {e.message}" for e in v.iter_errors(data)]

def validate_report_semantics(report):
    errors, indexes = [], {}
    keys = {"research_tasks":"research_task_id","research_attempts":"attempt_id","sources":"source_id","retrievals":"retrieval_id","evidence":"evidence_id","claims":"claim_id","legal_authorities":"authority_id","legal_propositions":"proposition_id","jurisdiction_assessments":"jurisdiction_assessment_id","assessments":"assessment_id","findings":"finding_id","human_reviews":"review_id"}
    for collection,key in keys.items():
        index={}
        for i,row in enumerate(report.get(collection,[])):
            value=row.get(key)
            if not isinstance(value,str): errors.append(f"{collection}[{i}].{key}: missing ID")
            elif value in index: errors.append(f"{collection}: duplicate ID {value}")
            else: index[value]=row
        indexes[collection]=index
    def refs(src,field,dst):
        for i,row in enumerate(report.get(src,[])):
            for ref in row.get(field,[]) or []:
                if ref not in indexes[dst]: errors.append(f"{src}[{i}].{field}: unresolved {dst} ID {ref}")
    pairs=[("research_attempts","research_task_id","research_tasks"),("retrievals","source_id","sources"),("evidence","retrieval_id","retrievals"),("claims","evidence_ids","evidence"),("legal_propositions","authority_ids","legal_authorities"),("jurisdiction_assessments","legal_proposition_ids","legal_propositions"),("assessments","claim_ids","claims"),("assessments","evidence_ids","evidence"),("assessments","legal_proposition_ids","legal_propositions"),("findings","assessment_ids","assessments"),("findings","jurisdiction_assessment_ids","jurisdiction_assessments"),("findings","supporting_evidence_ids","evidence"),("findings","contrary_evidence_ids","evidence")]
    for pair in pairs: refs(*pair)
    for i,f in enumerate(report.get("findings",[])):
        if f.get("assessment_status")=="supported_concern":
            if not f.get("supporting_evidence_ids"): errors.append(f"findings[{i}]: supported concern requires evidence")
            if not f.get("assessment_ids"): errors.append(f"findings[{i}]: supported concern requires assessment")
    for i,j in enumerate(report.get("jurisdiction_assessments",[])):
        if j.get("applicability_status") in {"applicable_supported","not_applicable_supported"} and not j.get("legal_proposition_ids"):
            errors.append(f"jurisdiction_assessments[{i}]: supported applicability requires legal propositions")
    for i,t in enumerate(report.get("research_tasks",[])):
        if t.get("status") in {"partial","blocked","failed"} and not t.get("blocked_reason"):
            errors.append(f"research_tasks[{i}]: status requires blocked_reason")
    return errors

def validate_report(report):
    return validate_schema(report)+validate_report_semantics(report)
