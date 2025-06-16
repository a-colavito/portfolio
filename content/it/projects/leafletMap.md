---
date: 2024-10-10
description: Start of the project for mapping Poliba resources using Leaflet
image: https://res.cloudinary.com/dkkvkj82k/image/upload/v1749552452/Screenshot_2025-06-10_alle_12.46.47_hqonwp.png
title: Simple Mapping Project
---

<img src = "https://res.cloudarinary.com/dkkvkj82k/image/upload/v1749552452/screenshot_2025-06-10_alle_12.46.47_hqonwp.png" style = width: 100%; altezza: 30%">
<a href = "https://mappegeneral.netlify.app"> È possibile utilizzare l'app qui </a>

# Mappando le biblioteche

Questo progetto si concentra sulla visualizzazione delle mappe della biblioteca dell'Università usando ** OpenStreetMap ** e la Biblioteca JavaScript ** Leaflet **.

## Struttura del progetto

L'intero progetto è contenuto nella cartella ** SbamAppe **, che include i file HTML per le quattro mappe della biblioteca universitaria. All'interno di questa cartella ci sono tre sottocartelle:

- ** set di dati **
- ** script **
- ** stile **

Cartella di dati ### ** **

Questa cartella contiene la sottocartella ** Percorsi **, che a sua volta include file JS con variabili (denominati identicamente al file) per inizializzare ** Geojson ** Dati per i percorsi. Tutti i dati su punti, poligoni, risorse e percorsi vengono estratti da questi file.

Cartella ### ** Script **

La cartella ** script ** contiene un singolo file, ** maplogic.js **, che gestisce la logica della mappa. Le principali funzionalità di questo file includono:

- ** costruttore di mappe **: una funzione che prende parametri come `Centercoordinates`,` zoomlevel`, ecc., Per impostare i livelli di foglietto e determinare come la libreria è rappresentata sulla mappa e nel menu a discesa.
- ** Aggiunta di livelli personalizzati ** alla mappa.
- ** Gestione del menu a discesa **: consente di attivare il menu e inizializzare i percorsi, visualizzando le informazioni relative alla libreria.
- ** Personalizzazione della funzione del volantino **: estende la libreria di foglietti con personalizzazioni specifiche.

La funzione del costruttore semplifica l'inizializzazione della mappa, consentendo la personalizzazione attraverso i parametri passati alla funzione ** InitializeMap **. Questo approccio rende il codice HTML più pulito e facilita l'aggiunta di nuove risorse semplicemente chiamando lo script nel file HTML della nuova risorsa.

Cartella ### ** stile **

La cartella ** Style ** contiene il file ** SBACSS **, che gestisce l'aspetto del menu della mappa e implementa la classe `.hidden`, essenziale affinché la funzionalità a disattivazione funzioni correttamente insieme a ** maplogic.js **.

Il foglio di stile include il colore del marchio di Politecnico di Bari per l'intestazione del menu e un carattere di prova (che può essere rimosso in modo sicuro per evitare conflitti).

** Nota: ** La dimensione della mappa non è gestita nel foglio di stile ma è invece definita direttamente nel file HTML per comodità.

### File HTML della libreria individuale

I file HTML per ogni libreria sono molto semplici. Importano librerie e fogli di stile e popolano il contenuto di HTML attraverso la funzione ** InitializeMap **.

Tutti gli elementi nel menu a discesa sono generati dalla funzione ** InitializeMap **. Inoltre, il menu e il contenitore della mappa sono strutturati gerarchicamente in modo da rimanere "allegati" l'uno all'altro.

## scelte aggiuntive e informazioni utili

- I percorsi sono stati creati utilizzando l'API di Google Maps.  
- Il file ** maplogic.js ** viene accuratamente commentato, in quanto ci sono alcune situazioni in cui il comportamento del volantino doveva essere annullato per applicare regole personalizzate (ad esempio, marcatori rossi e percorsi usando il colore di Politecnico di Bari).
- Le librerie vengono importate dal Web, ma potrebbe essere più efficiente scaricarle localmente su un server universitario. Non essendo particolarmente esperto nello sviluppo web, non posso dire quale soluzione sarebbe meglio ottimizzare il caricamento.

## possibili sviluppi futuri per la mappatura dell'intero Politecnico

Secondo me, ci sono due opzioni per mappare l'intera università:

1. ** Usa i progetti CAD di Politecnico **: questi potrebbero essere aggiunti come livelli personalizzati su OpenStreetMap usando il volantino.  
2. ** Estrai dati Geojson dall'app BefreeCampus **: porta l'app sul Web, potenzialmente come WebApp o utilizzando soluzioni come Flutter / React native per renderlo disponibile su più dispositivi.

Entrambe le opzioni offrono pro e contro. L'estrazione di dati Geojson e la mappatura dell'università tramite codice fornisce una grande modularità e facilità nella modifica delle posizioni delle risorse (ad esempio, se gli uffici vengono spostati, non è necessario richiedere un nuovo progetto, aggiornare solo il codice). D'altra parte, l'implementazione della mappa utilizzando i progetti offre una maggiore visibilità sui punti di accesso come scale ed ascensori e consente di incorporare risorse in un contesto dettagliato.

Entrambe le soluzioni consentirebbero la mappatura di ciascun piano e migliorare il riferimento alle risorse, sia in termini di accessibilità che di supporto per gli utenti esterni e interni nelle strutture di localizzazione.

La combinazione di opuscolo e OpenStreetMap fornisce un quadro solido per entrambe le soluzioni.

## contatto

Per eventuali richieste di informazioni, [Inviami un'e -mail] (Mailto: adolfocolavito@hotmail.it).