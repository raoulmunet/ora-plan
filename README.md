# ora-plan

[![tests](https://github.com/raoulmunet/ora-plan/actions/workflows/tests.yml/badge.svg)](https://github.com/raoulmunet/ora-plan/actions/workflows/tests.yml) ![Python](https://img.shields.io/badge/Python-3.10--3.13-blue) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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

## Oracle Dev Tools family

This repository is part of the **Oracle Dev Tools** suite: small, composable developer utilities designed around Oracle Database 19c, 23ai and 26ai.

| Area | Tools |
|---|---|
| Foundation | [ora-core](https://github.com/raoulmunet/ora-core) |
| SQL analysis | [ora-impact](https://github.com/raoulmunet/ora-impact) · [ora-plan](https://github.com/raoulmunet/ora-plan) · [ora-lineage](https://github.com/raoulmunet/ora-lineage) · [ora-lint](https://github.com/raoulmunet/ora-lint) · [ora-sql-diff](https://github.com/raoulmunet/ora-sql-diff) · [ora-sql-complexity](https://github.com/raoulmunet/ora-sql-complexity) · [ora-join-viz](https://github.com/raoulmunet/ora-join-viz) · [ora-bind](https://github.com/raoulmunet/ora-bind) |
| Data & operations | [ora-doc](https://github.com/raoulmunet/ora-doc) · [ora-data-quality](https://github.com/raoulmunet/ora-data-quality) · [ora-csv-loader](https://github.com/raoulmunet/ora-csv-loader) · [ora-etl-log](https://github.com/raoulmunet/ora-etl-log) · [ora-migration-check](https://github.com/raoulmunet/ora-migration-check) · [ora-errors](https://github.com/raoulmunet/ora-errors) · [ora-schema-explorer](https://github.com/raoulmunet/ora-schema-explorer) |
| PL/SQL analysis | [ora-exception-flow](https://github.com/raoulmunet/ora-exception-flow) · [ora-call-graph](https://github.com/raoulmunet/ora-call-graph) · [ora-dead-code](https://github.com/raoulmunet/ora-dead-code) |

## License

MIT.
