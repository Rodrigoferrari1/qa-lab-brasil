# QA Lab Brasil 3.5.0 — Knowledge Expansion (candidate)

Base: user-provided 3.4.0 production archive.

## Changes
- New trilingual topics: Legacy Systems, Version Control, Databricks, Playwright MCP.
- Expanded existing Data Lake topic (no duplicate); retained existing Git & GitHub topic.
- Added entries only to existing navigation groups; refreshed topic JSON cache key.
- No changes to QA Games, CTFL, Logic Lab, styles or unrelated assets.

## Practical setup guides
### Data Lake
A data lake is an architecture, not a single executable to install. Use a test cloud account and budget alerts. Create private object storage, least-privilege access, audit logging, raw/curated folders and upload synthetic data. Validate row counts, schema, permissions, duplicate ingestion and reprocessing. See provider documentation: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html ; https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-introduction ; https://cloud.google.com/storage/docs .

### Databricks
Use https://docs.databricks.com/ to select cloud/region/workspace options and verify current compute and billing. In a notebook run `SELECT 1 AS teste;`. For PySpark, `df = spark.createDataFrame([(101,120.0),(102,50.0)], ["id","valor"])` and `display(df)`. Persist only to an authorized test schema. Test data quality and reconcile sources and targets.

### Version Control
Download Git at https://git-scm.com/downloads . Run `git --version`, `git init`, `git status`, `git add .`, `git commit -m "Initial version"` in a disposable project. Never commit secrets.

### Playwright MCP
See https://github.com/microsoft/playwright-mcp . Install supported Node.js LTS. Confirm `node --version` and `npx --version`. In a compatible MCP client, use command `npx` with args `["@playwright/mcp@latest"]`, according to the client's current server configuration format. Restrict use to authorized QA sites; do not expose credentials.

## Validation checklist
- PT/EN/ES topic rendering, search and nav
- Existing Git, Playwright, Data Lake topics remain accessible
- Web/mobile menu and topic routing
- QA Games, CTFL, Logic Lab smoke regression
- BrowserStack final verification before production
