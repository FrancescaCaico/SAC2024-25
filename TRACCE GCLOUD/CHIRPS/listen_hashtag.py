import re
import sys
from google.cloud import pubsub_v1
import os

hash = sys.argv[1]
subscriber = pubsub_v1.SubscriberClient()

# Configura il progetto e la sottoscrizione
subscription_path = subscriber.subscription_path("chirpsfc", hash+'subs')

try:
    subscription = subscriber.create_subscription(
        request={"name": subscription_path, "topic": f"projects/chirpsfc/topics/{hash}"}
    )
except:
    print("Subs already created")

# Funzione di Callback
def callback(message):
    try:
       data = message.data.decode('utf-8')
       for h in re.findall('(#\w+)', data, re.DOTALL): 
           print(f"Nuovo messaggio in topic {h}: \'{data}\'")
       message.ack()

    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.