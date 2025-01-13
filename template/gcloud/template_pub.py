from google.cloud import pubsub_v1

topic_name=os.environ['TOPIC'] if 'TOPIC_NAME' in os.environ.keys() else 'updates'
project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'travelscf'

publisher= pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('travelscf', 'updates')


  future = publisher.publish(topic_path, data=json.dumps(data).encode('utf-8'))
        print(f"[Pub/Sub] Notifica inviata con ID: {future.result()}")
