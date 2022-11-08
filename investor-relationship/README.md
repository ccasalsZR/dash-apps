

gcloud builds submit --tag gcr.io/docmorriscare/investor-relations  --project=docmorriscare

gcloud run deploy --image gcr.io/docmorriscare/investor-relations --platform managed  --project=docmorriscare --allow-unauthenticated