# To deploy the cloud function use this command

SERVICE_ACCOUNT="$(gcloud storage service-agent --project=jdiaz-sandbox-402617)"

gcloud projects add-iam-policy-binding jdiaz-sandbox-402617 \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role='roles/pubsub.publisher'
    
gcloud functions deploy process_invoice --gen2 --region=us-east1 \
--runtime=python312 \
--source=. \
--entry-point=trigger_gcs \
--trigger-bucket=carvajal-demo-input