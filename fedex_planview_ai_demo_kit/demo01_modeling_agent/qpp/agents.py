import os

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
except Exception:
    vertexai = None
    GenerativeModel = None

from prompts import SYSTEM_CONTEXT, SOURCE_ANALYSIS_PROMPT, MODELING_PROMPT, QUALITY_PROMPT, REVIEW_PROMPT

class GeminiClient:
    def __init__(self):
        self.project_id = os.getenv('PROJECT_ID')
        self.region = os.getenv('REGION', 'us-central1')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.offline = os.getenv('OFFLINE_MODE', 'true').lower() == 'true'
        if not self.offline and vertexai:
            vertexai.init(project=self.project_id, location=self.region)
            self.model = GenerativeModel(self.model_name, system_instruction=SYSTEM_CONTEXT)
        else:
            self.model = None

    def generate(self, prompt: str) -> str:
        if self.offline or self.model is None:
            return self._mock_response(prompt)
        resp = self.model.generate_content(prompt)
        return resp.text

    def _mock_response(self, prompt: str) -> str:
        if 'source analysis table' in prompt:
            return """| field_name | likely_business_meaning | target_bigquery_type | quality_concerns | confidence |
|---|---|---:|---|---:|
| logbookId | Unique log entry identifier | STRING | Must be non-null and unique | High |
| projectId | Project associated with the log entry | STRING | Must resolve to project master | High |
| logType | Risk, Issue, Decision, Dependency, or Assumption | STRING | Controlled vocabulary validation | Medium |
| logStatus | Current lifecycle state of the entry | STRING | Must map to canonical status | Medium |
| severity | Business impact level | STRING | Critical/High values should drive alerts | Medium |
| createdDate | Entry creation date | DATE | Cannot be in future | High |
| resolvedDate | Resolution/closure date | DATE | Should be null for open entries | Medium |
| summaryText | Narrative description | STRING | PII/sensitive text review may be required | Medium |"""
        if 'propose a BigQuery Silver table' in prompt:
            return """## Proposed model

**Silver grain:** one row per Logbook entry.

**Gold model:** `fact_logbook` linked to `dim_project`, `dim_log_type`, `dim_status`, and `dim_date`.

**Partitioning:** partition Silver/Gold fact by `created_date`.

**Clustering:** cluster by `project_id`, `log_status`, `severity`.

```sql
CREATE OR REPLACE TABLE planview_silver.logbook (
  logbook_id STRING NOT NULL,
  project_id STRING,
  log_type STRING,
  log_status STRING,
  severity STRING,
  owner_name STRING,
  created_date DATE,
  resolved_date DATE,
  summary_text STRING,
  source_system STRING,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) PARTITION BY created_date
CLUSTER BY project_id, log_status, severity;
```"""
        if 'data quality rules' in prompt:
            return """| Rule ID | Rule | Severity | SQL Pattern |
|---|---|---|---|
| DQ-001 | logbook_id must be non-null | Critical | `logbook_id IS NULL` |
| DQ-002 | project_id must resolve to project | High | anti-join to project master |
| DQ-003 | resolved_date cannot be before created_date | High | `resolved_date < created_date` |
| DQ-004 | open items should not have resolved_date | Medium | `log_status IN (...) AND resolved_date IS NOT NULL` |
| DQ-005 | severity must use approved values | Medium | not in approved severity list |"""
        return """| Area | Finding | Recommendation |
|---|---|---|
| Security | Narrative fields may contain sensitive content | Classify text fields and avoid sending raw sensitive data to the model |
| Governance | Synthetic data product needs business owner and glossary | Register product metadata in Knowledge Catalog/Dataplex |
| Reuse | Gold entities should be reusable across Financial and AgilePlace products | Define shared Project and Date dimensions |
| Performance | Logbook queries will filter heavily by project/date/status | Partition by created date and cluster by project/status/severity |
| Human-in-loop | AI recommendations should not auto-promote production DDL | Require architect approval before deployment |"""


def run_modeling_workflow(sample_json: str):
    client = GeminiClient()
    source = client.generate(SOURCE_ANALYSIS_PROMPT.format(sample_json=sample_json))
    model = client.generate(MODELING_PROMPT.format(source_analysis=source))
    quality = client.generate(QUALITY_PROMPT)
    review = client.generate(REVIEW_PROMPT)
    return source, model, quality, review
