CREATE OR REPLACE TABLE `${PROJECT_ID}.planview_silver.project` (
  project_id STRING NOT NULL,
  project_name STRING,
  program_id STRING,
  health STRING,
  phase STRING,
  owner STRING
);

CREATE OR REPLACE TABLE `${PROJECT_ID}.planview_silver.logbook` (
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
);

CREATE OR REPLACE TABLE `${PROJECT_ID}.planview_silver.financial` (
  project_id STRING,
  fiscal_year INT64,
  fiscal_month INT64,
  budget_amount NUMERIC,
  forecast_amount NUMERIC,
  actual_amount NUMERIC,
  capex_opex STRING
);

CREATE OR REPLACE TABLE `${PROJECT_ID}.planview_silver.agileplace_work_item` (
  work_item_id STRING NOT NULL,
  project_id STRING,
  parent_work_item_id STRING,
  work_item_type STRING,
  title STRING,
  state STRING,
  blocked_flag BOOL,
  created_date DATE,
  closed_date DATE,
  story_points INT64
);

CREATE OR REPLACE VIEW `${PROJECT_ID}.planview_gold.project_health_summary` AS
SELECT
  p.project_id,
  p.project_name,
  p.health,
  p.phase,
  COUNTIF(l.log_status IN ('Open','Blocked','In Review')) AS active_logbook_items,
  COUNTIF(l.severity IN ('High','Critical') AND l.log_status IN ('Open','Blocked','In Review')) AS high_risk_active_items,
  SUM(f.forecast_amount) AS total_forecast,
  SUM(f.budget_amount) AS total_budget,
  SAFE_DIVIDE(SUM(f.forecast_amount)-SUM(f.budget_amount), SUM(f.budget_amount)) AS forecast_budget_variance_pct,
  COUNTIF(a.blocked_flag) AS blocked_work_items
FROM `${PROJECT_ID}.planview_silver.project` p
LEFT JOIN `${PROJECT_ID}.planview_silver.logbook` l USING(project_id)
LEFT JOIN `${PROJECT_ID}.planview_silver.financial` f USING(project_id)
LEFT JOIN `${PROJECT_ID}.planview_silver.agileplace_work_item` a USING(project_id)
GROUP BY 1,2,3,4;
