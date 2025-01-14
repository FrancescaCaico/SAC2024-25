from google.cloud import pubsub_v1
import argparse
import json
import os

# Configura le credenziali Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# Configura il progetto e la sottoscrizione
PROJECT_ID = "umcant"    # Sostituisci con il tuo Project ID
SUBSCRIPTION_ID = "newCantSub"

# Funzione di Callback
def callback(message):
    try:
        dati = json.loads(message.data.decode("utf-8"))
        cap = str(dati.get("cap", ""))

        if not FILTER_CAP or cap in FILTER_CAP:
            print(f"[NOTIFICA] Cantiere trovato con CAP {cap}: {dati}")
        

        message.ack()

    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")


# Configurazione del client e avvio dell'ascolto
if __name__ == "__main__":
    # Leggi i CAP dalla linea di comando (opzionale)
    parser = argparse.ArgumentParser(description="Client Umarell per ricevere notifiche")
    parser.add_argument('--cap', nargs='*', help='Lista di CAP per filtrare i messaggi (opzionale)')
    args = parser.parse_args()

    # Inizializza il set dei CAP (se specificati)
    FILTER_CAP = set(args.cap) if args.cap else set()

    # Configura il client Pub/Sub
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print(f"In ascolto su {subscription_path} per CAP: {FILTER_CAP if FILTER_CAP else 'Tutti i CAP'}...\n")

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