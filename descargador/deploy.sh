#!/usr/bin/env bash
# Despliega el backend en Cloud Run y la página en Firebase Hosting.
#
#   PROYECTO=mi-proyecto-firebase ./deploy.sh
#
# Requisitos: gcloud y firebase-tools instalados, sesión iniciada
# (gcloud auth login / firebase login) y plan Blaze en el proyecto.
# La región tiene que coincidir con la de firebase.json.
set -euo pipefail

: "${PROYECTO:?Definí PROYECTO=<id de tu proyecto de Firebase>}"
REGION="${REGION:-southamerica-east1}"
SERVICIO="descargador-api"

cd "$(dirname "$0")"

# Cloud Run guarda /tmp en memoria, así que los videos cuentan contra la memoria del contenedor.
gcloud run deploy "$SERVICIO" \
  --source . \
  --project "$PROYECTO" \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --concurrency 4 \
  --max-instances 3

firebase deploy --only hosting --project "$PROYECTO"
