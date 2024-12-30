export PROJECT_ID=travelscf
export TOPIC_NAME=updates
export SUBSCRIPTION_NAME=updateSub
export FUNCTION_NAME=update_db
export RUNTIME=python39
export EVENT_TYPE=providers/cloud.firestore/eventTypes/document.create


# # creazione topic 
# gcloud pubsub topics create ${TOPIC_NAME}

# # creazione sottoscrizione
# gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic=${TOPIC_NAME}

# deploy della funzione che risponde al fatto di aver inserito un nuovo documento nella collezione di riferimento
# gcloud functions deploy ${FUNCTION_NAME} --runtime ${RUNTIME} --trigger-event "${EVENT_TYPE}" --trigger-resource "projects/${PROJECT_ID}/databases/(default)/documents/updates/{documentId}" --docker-registry=artifact-registry --no-gen2 --region europe-west2

#FUNZIONE CHE RISPONDE AL FATTO DI AVER PUBBLICATO UN MESSAGGIO SUL TOPIC 
gcloud functions deploy ${FUNCTION_NAME} \
  --runtime ${RUNTIME} \
  --trigger-topic ${TOPIC_NAME} \
  --docker-registry=artifact-registry --no-gen2 --region europe-west2

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!/bin/bash
export NAME=webuser
export PROJECT_ID=travelscf
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"
touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
