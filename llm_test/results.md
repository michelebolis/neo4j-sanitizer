# LLM TEST

## ChatGPT

- Test 1: non esegue le query per errore di sintassi, non ci sono "WITH" tra "MATCH" e "SET"  
- Test 2: riportando l'errore riscontrato e chiedendo una correzione, le query non venivano modificate per correggere l'errore
- Test 3: proponendo di aggiungere un ";" dopo ogni SET, questa modifica viene correttamente eseguita.

Senza specificare che tipo di sanitizzazione applicare, ha settato tutte le proprietà considerate pericolose come NULL.

- Test 4: specificando la tipologia di sanitizzazione, cioè rimuovere le proprietà, ha generato delle query corrette.

## Gemini

- Test 1: le query sono esegubili e funzionanti. A differenza degli altri, utilizza autonomamente dopo ogni query il ";" in modo da poter eseguire tutto il codice. Senza specificare che tipo di sanitizzazione applicare, ha settato tutte le proprietà considerate pericolose a null
- Test 2: gli chiedo di rimuovere le proprietà invece che settarle a null. Mon è stato in grado di restituire solo il codice.  
- Test 3: specificando l'errore del limite di memoria riscontrato utilizza un semplice LIMIT che non rimuoverebbe tutte le poprietà.
- Test 4: suggerendo l'utilizzo di APOC e la sintassi da seguire, è riuscito ad utilizzare la procedura corretta in modo da generare query che sanitizzino la base di dati. E' stato necessario specificare nuovamente la struttura della base di dati e negare l'utilizzo di YIELD.

## Claude

- Test 1: non esegue le query per errore di sintassi, non ci sono "WITH" tra "MATCH" e "SET". Ha restituito solo il codice.  
- Test 2: facendogli notare l'errore, ha corretto le query aggiungendo un WITH dummy perchè ha capito che non servivano informazioni da salvare per le query successive

Senza specificare che tipo di sanitizzazione applicare, ha settato tutte le proprietà considerate pericolose come 'REDACTED'.  

- Test 3: specificando la tipologia di sanitizzazione, cioè rimuovere le proprietà, ha generato delle query ma con lo stesso errore del test 1.
- Test 4: specificando nuovamente l'errore, lo ha risolto ma dopo 5 ore non termina l'esecuzione.  
- Test 5: chiedendo se fosse possibile un'ottimizzazione, ha raggruppato alcune query ma l'esecuzione era ancora inefficiente
- Test 6: specificando l'utilizzo del ";", sono state generate delle query corrette ma per una transazione si è raggiunto il limite di memoria
- Test 7 + 8: specificando l'errore del limite di memoria, non riesce a risolverlo anzi restituendo query in cui viene aggiunto un semplice LIMIT
- Test 9: suggerendo l'utilizzo di APOC, è riuscito ad utilizzare la procedura corretta in modo da generare query che sanitizzino la base di dati.  
