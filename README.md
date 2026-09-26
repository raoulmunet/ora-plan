# ora-plan

Explain Oracle execution plans in plain language and flag structural patterns worth reviewing.

> **Oracle compatibility**
>
> | Oracle version | Support |
> |---|---|
> | Oracle Database 19c | ✅ Supported for common DBMS_XPLAN text formats |
> | Oracle Database 23ai | ✅ Supported for common DBMS_XPLAN text formats |
> | Oracle AI Database 26ai | ✅ Supported for common DBMS_XPLAN text formats |
>
> The parser is intentionally text-based and offline. If a future feature depends on plan columns or runtime statistics available only in specific releases, that difference will be documented here explicitly.

## Features

- parses common `DBMS_XPLAN.DISPLAY` / `DISPLAY_CURSOR` text output;
- extracts operation, object, rows and cost when present;
- explains Full Table Scan, Index Range Scan, Nested Loops, Hash Join, Sort, Filter and related operations;
- reports review hints without pretending that every full scan or hash join is a problem;
- text and JSON output;
- no database connection required.

## Installation

```bash
python -m pip install "git+https://github.com/raoulmunet/ora-plan.git"
```

## Usage

```bash
ora-plan examples/sample_plan.txt
ora-plan examples/sample_plan.txt --format json
cat plan.txt | ora-plan -
```

## Example

Input:

```text
| Id | Operation         | Name      | Rows | Cost |
|  0 | SELECT STATEMENT  |           |   10 |   12 |
|* 1 |  TABLE ACCESS FULL| CUSTOMERS |   10 |   12 |
```

Output:

```text
1. TABLE ACCESS FULL on CUSTOMERS
   Meaning: Oracle is scanning the table rather than using an index access path.
   Review: This can be perfectly valid for small tables or large-result queries; review only if the table is large and selectivity is high.
```

## Scope

This tool explains plan structure; it does **not** claim to determine the best plan automatically. Correct tuning still depends on table sizes, statistics, predicates, cardinality estimates, skew, bind values, partitioning and workload context.

## License

MIT.
