export PROJECT_ID=travelscf
export FUNCTION_NAME=update_db
export RUNTIME=python39
export EVENT_TYPE=providers/cloud.firestore/eventTypes/document.create

# deploy della funzione che risponde al fatto di aver inserito un nuovo documento nella collezione di riferimento
# gcloud functions deploy ${FUNCTION_NAME} --runtime ${RUNTIME} --trigger-event "${EVENT_TYPE}" --trigger-resource "projects/${PROJECT_ID}/databases/(default)/documents/updates/{documentId}" --docker-registry=artifact-registry --no-gen2 --region europe-west2

#FUNZIONE CHE RISPONDE AL FATTO DI AVER PUBBLICATO UN MESSAGGIO SUL TOPIC 

# gcloud functions deploy ${FUNCTION_NAME} \
#   --runtime ${RUNTIME} \
#   --trigger-topic ${TOPIC_NAME} \
#   --docker-registry=artifact-registry --no-gen2 --region europe-west2