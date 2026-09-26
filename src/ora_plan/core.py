from __future__ import annotations
from dataclasses import dataclass, asdict
import re

@dataclass(frozen=True)
class PlanStep:
    id: int
    operation: str
    name: str | None = None
    rows: str | None = None
    cost: str | None = None
    meaning: str | None = None
    review: str | None = None
    def to_dict(self): return asdict(self)

EXPLANATIONS = {
    "TABLE ACCESS FULL": (
        "Oracle is scanning table blocks rather than using an index access path.",
        "Valid for small tables or large-result queries; review if the table is large and predicates are highly selective."
    ),
    "INDEX RANGE SCAN": (
        "Oracle is scanning a bounded range of index entries.",
        "Usually appropriate for selective range/equality predicates; confirm table lookup cost and clustering factor when performance matters."
    ),
    "NESTED LOOPS": (
        "Oracle is repeatedly probing the inner row source for rows from the outer row source.",
        "Often good for selective outer inputs; review if the outer row count is much larger than estimated."
    ),
    "HASH JOIN": (
        "Oracle is building a hash structure for one row source and probing it with another.",
        "Often efficient for larger joins; review memory/cardinality estimates rather than treating the join type itself as a problem."
    ),
    "SORT": (
        "Oracle performs an explicit sort operation.",
        "Review if row counts are large or TEMP usage is material."
    ),
    "FILTER": (
        "Oracle applies a predicate or correlated condition to a row source.",
        "Inspect predicates and estimated/actual rows when available."
    ),
}

def _explain(operation: str):
    op=operation.upper().strip()
    for key,(meaning,review) in EXPLANATIONS.items():
        if key in op:
            return meaning,review
    return "Oracle execution-plan operation.", "Interpret together with predicates, cardinality and runtime statistics."

def parse_plan(text: str) -> list[PlanStep]:
    steps=[]
    for line in text.splitlines():
        if "|" not in line: continue
        cells=[c.strip() for c in line.strip().strip("|").split("|")]
        if not cells: continue
        m=re.fullmatch(r"\*?\s*(\d+)", cells[0])
        if not m or len(cells)<2: continue
        op=cells[1].strip()
        if not op or op.upper()=="OPERATION": continue
        name=cells[2].strip() if len(cells)>2 and cells[2].strip() else None
        rows=cells[3].strip() if len(cells)>3 and cells[3].strip() else None
        cost=cells[4].strip() if len(cells)>4 and cells[4].strip() else None
        meaning,review=_explain(op)
        steps.append(PlanStep(int(m.group(1)),op,name,rows,cost,meaning,review))
    return steps
