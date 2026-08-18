#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?Set PROJECT_ID}"
: "${REGION:=us-central1}"
: "${BQ_LOCATION:=US}"

gcloud config set project "$PROJECT_ID"

gcloud services enable   aiplatform.googleapis.com   bigquery.googleapis.com   storage.googleapis.com   run.googleapis.com   artifactregistry.googleapis.com   cloudbuild.googleapis.com

echo "Enabled required APIs. Now run ./common/sql/load_to_bigquery.sh from repo root."
