gcloud builds submit --tag gcr.io/docmorriscare/logistics-de  --project=docmorriscare

gcloud run deploy --image gcr.io/docmorriscare/logistics-de --platform managed  --project=docmorriscare --allow-unauthenticated

# with VPN
gcloud run deploy --image gcr.io/docmorriscare/logistics-de --platform managed  --project=docmorriscare --allow-unauthenticated --vpc-connector=snowconnector1 --vpc-egress=all-traffic


# Documentation to set up STATIC ip
# https://cloud.google.com/run/docs/configuring/static-outbound-ip#command-line_1
# https://manel-lemin.medium.com/static-ip-for-cloudrun-service-7f615ed2823d
