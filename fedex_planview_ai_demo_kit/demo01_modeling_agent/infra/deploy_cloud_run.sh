#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?Set PROJECT_ID}"
: "${REGION:=us-central1}"
SERVICE="planview-logbook-modeling-agent"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/planview-ai-demo/${SERVICE}:latest"

gcloud artifacts repositories create planview-ai-demo --repository-format=docker --location="$REGION" --quiet || true
gcloud builds submit ../.. --tag "$IMAGE"
gcloud run deploy "$SERVICE" --image "$IMAGE" --region "$REGION" --allow-unauthenticated   --set-env-vars PROJECT_ID="$PROJECT_ID",REGION="$REGION",OFFLINE_MODE="false"
