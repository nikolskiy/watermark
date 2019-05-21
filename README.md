# Watermark App
Work in progress...

## Run using docker-compose
1) `pip install docker-compose` (working Docker is required)
2) `docker-compose up --build`
3) The app will be served locally at http://127.0.0.1:8080/

## Deploying to Google cloud run
`gcloud builds submit`

This is cool option but it assumes that you have `gcloud` installed and the cloud builder has correct permissions 
(https://cloud.google.com/run/docs/continuous-deployment).
