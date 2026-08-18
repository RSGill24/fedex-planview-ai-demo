SYSTEM_CONTEXT = """
You are an enterprise data architecture assistant. The dataset is synthetic and Planview-like.
Do not claim it represents FedEx's actual Planview operating model. Focus on architecture patterns,
BigQuery modeling, governance, and data product design.
"""

SOURCE_ANALYSIS_PROMPT = """
Analyze the following raw Logbook sample and infer a source analysis table with fields:
field_name, likely_business_meaning, source_type, target_bigquery_type, data_product_relevance,
quality_concerns, confidence. Return markdown.

RAW SAMPLE:
{sample_json}
"""

MODELING_PROMPT = """
Using the source analysis below, propose a BigQuery Silver table and Gold analytical model.
Include grain, candidate keys, dimensions/facts, suggested partitioning/clustering, and rationale.
Return concise markdown and one SQL DDL block.

SOURCE ANALYSIS:
{source_analysis}
"""

QUALITY_PROMPT = """
Generate data quality rules for a synthetic Planview Logbook data product. Include rule id,
rule description, SQL check pattern, severity, and downstream impact.
"""

REVIEW_PROMPT = """
Review the proposed Planview Logbook data product against enterprise architecture concerns:
security, governance, reuse, performance, data quality, cost, and migration to GCP.
Return risks and recommendations in a table.
"""
