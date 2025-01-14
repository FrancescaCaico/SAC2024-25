from google.cloud import pubsub_v1
import argparse
import json
import os

# Configura le credenziali Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# Configura il progetto e la sottoscrizione
PROJECT_ID = "uviaggiu"    # Sostituisci con il tuo Project ID
SUBSCRIPTION_ID = "updateSub"

# Funzione di Callback
def callback(message):
    try:
        
        messaggio = message.data.decode("utf-8")
        print(f"Messaggio ricevuto: {messaggio}")
        
        dati = json.loads(message.data.decode("utf-8"))
        
        print(f"[NOTIFICA] Modifica viaggio: {dati}")
       
        # Conferma che il messaggio è stato elaborato
        message.ack()

    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")


# Configurazione del client e avvio dell'ascolto
if __name__ == "__main__":
    # Configura il client Pub/Sub
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    # Avvia l'ascolto dei messaggi
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        # Attende indefinitamente
        streaming_pull_future.result()
    except KeyboardInterrupt:
        # Cancella il listener su interruzione
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        print(f"Errore durante l'ascolto: {e}")
        streaming_pull_future.cancel()