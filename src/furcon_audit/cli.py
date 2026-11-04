import argparse, json, sys
from pathlib import Path
from .validator import validate_report
from .markdown import render_markdown

def main():
    p=argparse.ArgumentParser(description="Validate and render a FurCon audit report")
    p.add_argument("input"); p.add_argument("--markdown"); a=p.parse_args()
    try: data=json.loads(Path(a.input).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        print(f"Input error: {exc}",file=sys.stderr); return 2
    errors=validate_report(data)
    if errors:
        print("\n".join(errors),file=sys.stderr); return 1
    if a.markdown: Path(a.markdown).write_text(render_markdown(data),encoding="utf-8")
    print("Schema and semantic validation passed."); return 0
if __name__=="__main__": raise SystemExit(main())
