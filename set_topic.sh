export TOPIC_NAME=santa
export SUBSCRIPTION_NAME=coordinatore

gcloud pubsub topics create ${TOPIC_NAME}
gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic=${TOPIC_NAME}