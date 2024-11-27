#PRINCIPALI COMANDI PER FAR PARTIRE GOOGLE CLOUD E L'AMBIENTE VIRTUALE
##AMBIENTE VIRTUALIZZATO
Per creare l'ambiente virtualizzato:  `python3 -m venv env`
Per lavorare all'interno dell'ambiente: `source env/bin/activate`
Per installare le dipendenze necessarie: `pip install -r requirements.txt`
Per far partire gli eseguibili: `python3 main.py`

##GOOGLE CLOUD
Per creare il progetto: 
1. inserire il nome del progetto in una variabile di ambiente per rendere tutto più semplice
   `export PROJECT_ID=<nome>`
2. Creare il progetto: `google cloud projects create $PROJECT_ID --set-as-default`
3. Generare il file APP.YAML con il seguente contenuto di esempio:
  `
   runtime: python311
   handlers: 
     - url: /.*
       secure: always
       script: auto `
4. Ricordasi di inserire il file *.gitcloudignore* con il seguente contenuto
`.git
  .gitignore
  __pycache__/
  env/
  /setup.cfg
  .gcloudignore `
5. Creare l'app per il progetto: `google cloud app create --project=$PROJECT_ID`
6. Eseguire il deploy del progetto: `google cloud app deploy`
