gcloud builds submit --tag gcr.io/docmorriscare/logistics-de  --project=docmorriscare

gcloud run deploy --image gcr.io/docmorriscare/logistics-de --platform managed  --project=docmorriscare --allow-unauthenticated