from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from .core import parse_plan

def main(argv=None):
    p=argparse.ArgumentParser(description="Explain Oracle DBMS_XPLAN text.")
    p.add_argument("source")
    p.add_argument("--format",choices=("text","json"),default="text")
    a=p.parse_args(argv)
    text=sys.stdin.read() if a.source=="-" else Path(a.source).read_text(encoding="utf-8")
    steps=parse_plan(text)
    if a.format=="json":
        print(json.dumps([s.to_dict() for s in steps],indent=2))
    else:
        for i,s in enumerate(steps,1):
            target=f" on {s.name}" if s.name else ""
            print(f"{i}. {s.operation}{target}\n   Meaning: {s.meaning}\n   Review: {s.review}")
    return 0
if __name__=="__main__": raise SystemExit(main())
