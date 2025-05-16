from google.cloud import pubsub_v1
import argparse
import json
import os
from dao import DAO
# questo subber pubblica sugli altri topic 
PROJECT_ID = "examcloudfc"   
SUBSCRIPTION_ID = "coordinatore"
dao = DAO()
publisher= pubsub_v1.PublisherClient()


def callback(message):
    try:
        
        messaggio = message.data.decode("utf-8")
        print(f"Messaggio ricevuto: {messaggio}")
        
        dati = json.loads(message.data.decode("utf-8"))
        
        print(f"[NOTIFICA] {dati}")
        
        # arriva l'email
        d = dao.getDestinatario(dati)
        print(d)
       
        message.ack()
        topic_path = publisher.topic_path('examcloudfc', f"{dati}")
        try: 
            publisher.create_topic(request={"name": topic_path})
        except: 
            print("topic già presente")
        
        publisher.publish(topic_path, (d.get("toEmail")).encode('utf-8'))

    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")


if __name__ == "__main__":
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        print(f"Errore durante l'ascolto: {e}")
        streaming_pull_future.cancel()