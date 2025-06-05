# Relazione Tecnica - Server HTTP in Python

## Descrizione Generale

Questo progetto implementa un semplice server HTTP multithread utilizzando Python, il modulo `socket` per la comunicazione di rete e il modulo `threading` per la gestione concorrente delle connessioni client. Il server è progettato per servire file statici da una directory specifica (in questo caso `www`).

## Componenti Principali

### Classe HTTPServer

La classe `HTTPServer` gestisce l'inizializzazione del server, l'accettazione delle connessioni e la gestione delle richieste HTTP.

- **`__init__`**: Inizializza il socket TCP e lo configura per l’ascolto sulla porta specificata.
- **`start()`**: Avvia un ciclo infinito in cui accetta nuove connessioni e le gestisce tramite thread separati.
- **`handle_request()`**: Elabora le richieste GET, recupera i file richiesti e invia la risposta HTTP.
- **`send_response()`**: Costruisce e invia la risposta HTTP, includendo intestazioni e corpo.

### Classe Logger

Il `Logger` fornisce un semplice sistema di logging con colori ANSI per evidenziare i messaggi di log nel terminale.

## Funzionalità Supportate

- Gestione richieste HTTP di tipo `GET`.
- Servizio di file statici (HTML, CSS, immagini, ecc.).
- Risposta con codice `404 Not Found` per file non esistenti.
- Risposta con codice `405 Method Not Allowed` per metodi diversi da GET.
- Logging colorato delle attività del server (connessioni, errori, richieste).

## Architettura e Concorrenza

Ogni nuova connessione viene gestita da un nuovo thread, permettendo al server di rispondere simultaneamente a più client. Questo è ottenuto tramite il modulo `threading`.

## Sicurezza e Limitazioni

- Non è implementata la validazione dei percorsi (path traversal potrebbe essere possibile).
- Non è supportato HTTPS.
- Il server non gestisce richieste POST o altre oltre GET.

## Avvio del Server

```python
if __name__ == "__main__":
    server = HTTPServer(HOST, PORT, WWW_ROOT)
    try:
        server.start()
    except KeyboardInterrupt:
        server.server_socket.close()
        server.logger.log("red", "Server stopped by user.")
```
## Coclusioni
Il progetto fornisce un punto di partenza per comprendere il funzionamento di un server HTTP e la gestione delle connessioni in Python. Può essere esteso per includere ulteriori funzionalità come routing dinamico, supporto a POST, e una migliore sicurezza