#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?Set PROJECT_ID}"
: "${BQ_LOCATION:=US}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="$SCRIPT_DIR/../data"

envsubst < "$SCRIPT_DIR/01_create_datasets.sql" | bq query --use_legacy_sql=false
envsubst < "$SCRIPT_DIR/02_create_tables.sql" | bq query --use_legacy_sql=false

bq load --source_format=CSV --skip_leading_rows=1 --replace "${PROJECT_ID}:planview_silver.project" "$DATA_DIR/planview_project.csv" project_id:STRING,project_name:STRING,program_id:STRING,health:STRING,phase:STRING,owner:STRING

bq load --source_format=CSV --skip_leading_rows=1 --replace "${PROJECT_ID}:planview_silver.logbook" "$DATA_DIR/planview_logbook.csv" logbook_id:STRING,project_id:STRING,log_type:STRING,log_status:STRING,severity:STRING,owner_name:STRING,created_date:DATE,resolved_date:DATE,summary_text:STRING,source_system:STRING

bq load --source_format=CSV --skip_leading_rows=1 --replace "${PROJECT_ID}:planview_silver.financial" "$DATA_DIR/planview_financial.csv" project_id:STRING,fiscal_year:INTEGER,fiscal_month:INTEGER,budget_amount:NUMERIC,forecast_amount:NUMERIC,actual_amount:NUMERIC,capex_opex:STRING

bq load --source_format=CSV --skip_leading_rows=1 --replace "${PROJECT_ID}:planview_silver.agileplace_work_item" "$DATA_DIR/agileplace_work_item.csv" work_item_id:STRING,project_id:STRING,parent_work_item_id:STRING,work_item_type:STRING,title:STRING,state:STRING,blocked_flag:BOOLEAN,created_date:DATE,closed_date:DATE,story_points:INTEGER

echo "Loaded synthetic Planview-like demo data into BigQuery."
