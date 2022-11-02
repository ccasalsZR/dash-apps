gcloud builds submit --tag gcr.io/docmorriscare/sandoz-hexal  --project=docmorriscare

gcloud run deploy --image gcr.io/docmorriscare/sandoz-hexal --platform managed  --project=docmorriscare --allow-unauthenticated