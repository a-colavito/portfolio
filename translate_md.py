import os
from pathlib import Path
from deep_translator import GoogleTranslator
import yaml
import re

MAX_CHARS = 4999  # Google Translate limit is 5000, stay safe

# --- DIZIONARIO DI TERMINI DA PROTEGGERE/SOSTITUIRE ---
# I valori dovrebbero essere sempre nella lingua del target, se noti errori
# nella traduzione di questi termini.
# Useremo questo per mappare termini originali a una versione preferita/corretta
# nella lingua target, o per proteggere nomi propri.
#
# Esempio:
# 'Politecnico di Bari': 'Polytechnic University of Bari' (per l'inglese)
# 'Leaflet': 'Leaflet'
# 'OpenStreetMap': 'OpenStreetMap'
# 'JavaScript': 'JavaScript'
# 'Google Maps APIs': 'Google Maps APIs'
# 'GeoJSON': 'GeoJSON'
# 'BefreeCampus': 'BefreeCampus'
# 'HTML': 'HTML'
# 'CSS': 'CSS'
#
# Nota: La chiave del dizionario deve essere il termine come appare nel testo SORGENTE,
# il valore è come DEVE apparire nel testo TARGET.
# Se un termine deve essere uguale in entrambe le lingue, mettilo comunque per protezione.
PROTECTED_TERMS_MAP = {
    # Termini generici indipendenti dalla lingua di partenza (se uguali in IT/EN)
    "Leaflet": "Leaflet",
    "OpenStreetMap": "OpenStreetMap",
    "JavaScript": "JavaScript",
    "GeoJSON": "GeoJSON",
    "BefreeCampus": "BefreeCampus",
    "HTML": "HTML",
    "CSS": "CSS",
    "JS": "JS",
    # Nomi di cartelle/file che non dovrebbero essere tradotti
    "dataset": "dataset",
    "script": "script",
    "Style": "Style", # "Style" in maiuscolo per il nome della cartella
    "Sbamappe": "Sbamappe",
    "Maplogic.js": "Maplogic.js",
    "SWEX": "SWEX",
    # Nomi istituzionali o specifici (se si traduce da italiano a inglese)
    "Politecnico di Bari": "Polytechnic University of Bari",
    "le librerie dell'Ateneo": "the university libraries", # Correzione specifica per frase
    # Traduzioni specifiche di frasi che Google Translator sbaglia
    "funzione costruttore": "constructor function", # Per "Map manufacturer"
    "toggle il menu": "toggle the menu", # Per "to toge the menu"
    "librerie": "libraries", # Per "bookcases" (context specific)
    "piantine": "floor plans", # Per "seedlings"
    "API di Google Maps": "Google Maps APIs", # Per "Google Maps bees"
    # Placeholder per link mailto
    "[send me an email](email: adolfocolavito@hotmail.it)": "[send me an email](mailto:adolfocolavito@hotmail.it)",
}

def extract_front_matter(text):
    """Estrae il front matter (intestazione YAML) dal contenuto Markdown."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        body = parts[2].lstrip("\n")
        return fm, body
    return {}, text

def split_text(text, max_chars=MAX_CHARS):
    """Divide il testo in blocchi più piccoli rispettando i paragrafi."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for p in paragraphs:
        # Aggiungi un piccolo buffer per la punteggiatura/spazi extra che Google potrebbe aggiungere
        if len(current) + len(p) + 5 < max_chars:
            current += p + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            current = p + "\n\n"

    if current:
        chunks.append(current.strip())

    return chunks

def translate(text, src, tgt):
    """
    Traduce il testo diviso in blocchi, evitando il limite dei 5000 caratteri.
    Implementa pre- e post-elaborazione per migliorare la qualità,
    preservando blocchi di codice, tag HTML e termini specifici.
    """
    code_block_placeholders = {}
    html_placeholders = {}
    term_placeholders = {}

    text_to_process = text

    # --- PRE-PROCESSAMENTO ---

    # 1. Nascondi i blocchi di codice (fenced code blocks: ```lang ... ```)
    # Protegge l'intero blocco, inclusi i delimitatori
    fenced_code_block_pattern = r"(```[a-zA-Z0-9]*\n[\s\S]*?\n```)"
    
    def replace_fenced_code_with_placeholder(match):
        code_block = match.group(0)
        placeholder = f"__CODE_BLOCK_{len(code_block_placeholders)}__" # Indice numerico più semplice
        code_block_placeholders[placeholder] = code_block
        return placeholder
    
    text_to_process = re.sub(fenced_code_block_pattern, replace_fenced_code_with_placeholder, text_to_process)

    # 2. Nascondi i tag HTML (es. <div>, <br/>, <img src = "..." Style = "...")
    # Questo pattern è più robusto per catturare attributi con o senza spazi intorno all'uguale
    html_tag_pattern = r"<(\w+)(?:\s+[^>]*?)*?>" # Cattura <tag eventuali_attributi>
    
    def replace_html_with_placeholder(match):
        tag = match.group(0)
        placeholder = f"__HTML_TAG_{len(html_placeholders)}__" # Indice numerico
        html_placeholders[placeholder] = tag
        return placeholder

    text_to_process = re.sub(html_tag_pattern, replace_html_with_placeholder, text_to_process, flags=re.IGNORECASE)


    # 3. Nascondi i termini specifici del PROTECTED_TERMS_MAP
    # Ordina i termini dalla più lunga alla più corta per evitare sostituzioni parziali
    # E per assicurare che "[send me an email](email: ...)" venga catturato prima
    sorted_terms = sorted(PROTECTED_TERMS_MAP.keys(), key=len, reverse=True)
    
    for term_src in sorted_terms:
        # Usa re.escape per trattare caratteri speciali nella stringa del termine come letterali
        # Aggiungi \b per word boundary per evitare di catturare "foo" in "foobar"
        # ma rimuovilo per i pattern che non sono parole intere (es. link mailto)
        if term_src.startswith("[send me an email]"): # Pattern specifico per il link mailto
            pattern = re.escape(term_src)
        else:
            pattern = r"\b" + re.escape(term_src) + r"\b"
            
        def replace_term_with_placeholder(match):
            original_match = match.group(0)
            placeholder = f"__TERM_{len(term_placeholders)}__"
            # Salviamo la forma corretta nella lingua target
            term_placeholders[placeholder] = PROTECTED_TERMS_MAP[term_src]
            return placeholder
        
        # Sostituisce solo la prima occorrenza per evitare problemi con le regex.
        # È più sicuro usare un ciclo while per sostituire tutte le occorrenze di un termine
        # fino a quando non ce ne sono più.
        while re.search(pattern, text_to_process):
            text_to_process = re.sub(pattern, replace_term_with_placeholder, text_to_process, 1) # Sostituisce una volta sola


    # --- TRADUZIONE ---
    parts = split_text(text_to_process) 
    translated_parts = []
    for part in parts:
        translated_parts.append(GoogleTranslator(source=src, target=tgt).translate(part))
    
    translated_text = "\n\n".join(translated_parts)

    # --- POST-PROCESSAMENTO ---

    # 1. Ripristina i termini specifici dal PROTECTED_TERMS_MAP
    # Ordina i placeholder per lunghezza (dal più lungo al più corto)
    # per evitare sostituzioni parziali se un placeholder è substring di un altro.
    sorted_placeholders = sorted(term_placeholders.keys(), key=len, reverse=True)
    for placeholder in sorted_placeholders:
        translated_text = translated_text.replace(placeholder, term_placeholders[placeholder])
        
    # 2. Ripristina i tag HTML dai placeholder
    # Vanno ripristinati in ordine casuale, l'importante è che i placeholder siano unici.
    for placeholder, original_tag in html_placeholders.items():
        translated_text = translated_text.replace(placeholder, original_tag)

    # 3. Ripristina i blocchi di codice dai placeholder
    # Anche qui l'ordine di ripristino non dovrebbe importare se i placeholder sono unici.
    for placeholder, original_code_block in code_block_placeholders.items():
        translated_text = translated_text.replace(placeholder, original_code_block)
        
    # 4. Correzione sintassi grassetto e corsivo (dopo tutti i ripristini)
    # Cerca ** testo ** e lo trasforma in **testo** (per il grassetto)
    translated_text = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', translated_text)
    # Cerca * testo * e lo trasforma in *testo* (per il corsivo)
    translated_text = re.sub(r'\*\s*(.*?)\s*\*', r'*\1*', translated_text)
    # Gestisce casi come **parola ** o *parola * (spazi prima del tag di chiusura)
    translated_text = re.sub(r'(\*\*|\*)\s*(\w+)\s*(\*\*|\*)', r'\1\2\3', translated_text)
    
    # Ulteriore pulizia per assicurare che non ci siano spazi extra tra parole e punteggiatura
    # (es. "parola ." -> "parola.")
    translated_text = re.sub(r'\s+([.,!?;:])', r'\1', translated_text)


    return translated_text

def process(src_dir, tgt_dir, src_lang, tgt_lang):
    """Processa tutti i file Markdown da una cartella sorgente a una di destinazione."""
    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir)
        tgt = Path(tgt_dir) / rel
        
        # Ignora i file già tradotti (se non vuoi sovrascriverli ogni volta)
        # Se vuoi rigenerare sempre i file, commenta o rimuovi la riga seguente
        # if tgt.exists(): 
        #      continue

        text = src.read_text(encoding="utf-8")
        fm, body = extract_front_matter(text)

        # ✨ Traduci il front matter (solo valori stringa)
        translated_fm = {}
        for key, value in fm.items():
            if isinstance(value, str):
                try:
                    # Per il front matter, applichiamo le stesse logiche di protezione termini
                    # e correzione grassetto/corsivo
                    # Non ci aspettiamo HTML o blocchi di codice qui, quindi non li processiamo per FM.
                    
                    # Sostituisci i termini protetti nel valore del front matter
                    processed_value = value
                    for term_src in sorted(PROTECTED_TERMS_MAP.keys(), key=len, reverse=True):
                        if term_src in processed_value: # Semplice controllo di inclusione per FM
                            processed_value = processed_value.replace(term_src, PROTECTED_TERMS_MAP[term_src])
                    
                    translated_value = GoogleTranslator(source=src_lang, target=tgt_lang).translate(processed_value)
                    
                    # Applica correzioni grassetto/corsivo
                    translated_value = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', translated_value)
                    translated_value = re.sub(r'\*\s*(.*?)\s*\*', r'*\1*', translated_value)
                    translated_value = re.sub(r'(\*\*|\*)\s*(\w+)\s*(\*\*|\*)', r'\1\2\3', translated_value)
                    translated_value = re.sub(r'\s+([.,!?;:])', r'\1', translated_value)
                    
                    translated_fm[key] = translated_value
                except Exception as e:
                    print(f"Errore durante la traduzione del front matter per '{key}': {e}")
                    translated_fm[key] = value
            else:
                translated_fm[key] = value  # Lascia invariato tutto il resto

        # Qui la funzione `translate` ora include tutta la logica di pre- e post-processamento
        trans_body = translate(body, src_lang, tgt_lang)

        # ⚠️ Nota automatica di traduzione
        if tgt_lang.lower() == "english":
            translation_note = "> ⚠️ *This content was automatically translated from Italian using a machine translation tool.*\n\n"
        elif tgt_lang.lower() == "italian":
            translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente dall’inglese tramite un sistema di traduzione automatica.*\n\n"
        else:
            translation_note = "> ⚠️ *This content was automatically translated.*\n\n"

        content = (
            "---\n"
            + yaml.dump(translated_fm, allow_unicode=True, default_flow_style=False, sort_keys=False) # Aggiunto sort_keys=False per mantenere l'ordine originale se preferito
            + "---\n\n"
            + translation_note
            + trans_body
        )

        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.write_text(content, encoding="utf-8")
        print(f"Tradotto {rel} da {src_lang} a {tgt_lang}")

if __name__ == "__main__":
    # Esempio di utilizzo:
    # Assicurati di avere una struttura di cartelle come:
    # content/it/tuo_file.md
    # content/en/
    # Esegui lo script per tradurre da italiano a inglese e viceversa.
    print("Avvio traduzione da italiano a inglese...")
    # Crea un file di esempio per testare
    example_it_content = """---
date: 2024-10-10
description: Inizio del progetto di mappatura delle risorse del Politecnico di Bari con Leaflet
image: https://res.cloudinary.com/dkkvkj82k/image/upload/v1749552452/screenshot_2025-06-10_alle_12.46.47_hqonwp.png
title: Progetto di mappatura semplice
---

> Questo è un testo di esempio con un link all'app.
<img src="https://res.cloudinary.com/dkkvkj82k/image/upload/v1749552452/screenshot_2025-06-10_alle_12.46.47_hqonwp.png" style="width: 100%; height: 30%;">
<a href="https://mappegeneral.netlify.app">qui puoi usare l'app</a>

# Librerie Mappa

Questo progetto riguarda la visualizzazione delle mappe delle **librerie dell'Ateneo**, usando le mappe **OpenStreetMap** e la libreria JavaScript **Leaflet**.

## Struttura del progetto

L'intero progetto è contenuto nella cartella **Sbamappe**, che include i file HTML per le quattro mappe delle biblioteche dell'Università. All'interno di questa cartella, ci sono tre altre sottocartelle:

- **dataset**
- **script**
- **Style**

### cartella **dataset**

Questa cartella contiene la sottocartella **Paths**, che a sua volta include file JS con variabili (nominate identiche al file) per inizializzare i dati **GeoJSON** relativi ai percorsi. Tutti i dati su punti, poligoni, risorse e percorsi sono estratti da questi file.

### Cartella **script**

La cartella **script** contiene un singolo file, **Maplogic.js**, che gestisce la logica delle mappe. Le caratteristiche principali di questo file includono:

- **Funzione costruttore mappa**: una funzione che accetta parametri come `centerCoordinates`, `zoomLevel`, ecc., per impostare i layer di Leaflet e determinare come la libreria è rappresentata sulla mappa e nel menu a discesa.
- **Aggiunta di layer personalizzati** alla mappa.
- **Gestione del menu a discesa**: consente di **toggle il menu** e inizializzare i percorsi, mostrando le informazioni relative alla libreria.
- **Personalizzazione delle funzioni** di Leaflet: estende la libreria Leaflet con personalizzazioni specifiche.

La funzione costruttore semplifica l'inizializzazione della mappa, consentendo di inserire personalizzazioni tramite parametri passati alla funzione **initializeMap**. Questo approccio rende il codice HTML più snello e facilita l'aggiunta di nuove risorse richiamando semplicemente lo script nel file HTML della nuova risorsa.

### Cartella **Style**

La cartella **Style** contiene il file **SWEX**, che gestisce l'aspetto del menu della mappa e implementa la classe ` .hidden`, essenziale per il corretto funzionamento del toggle sul menu insieme a **Maplogic.js**.

Il foglio di stile include il colore del **Politecnico di Bari** per l'intestazione del menu e un font di test (che può essere rimosso senza problemi per evitare conflitti).

**Nota:** La dimensione della mappa non è gestita nel foglio di stile, ma è definita direttamente nel file HTML per praticità.

### file HTML individuali delle librerie

I file HTML per ogni libreria sono molto semplici. Importano le librerie e i fogli di stile di Leaflet, quindi popolano il contenuto dell'HTML tramite la funzione **initializeMap**.

Tutti gli elementi nel menu a discesa sono generati dalla funzione **initializeMap**. Inoltre, il menu e il contenitore della mappa sono strutturati in modo gerarchico, in modo che rimangano "attaccati" l'uno all'altro.

## Ulteriori scelte e informazioni utili

- I percorsi sono stati creati utilizzando le **API di Google Maps**.
- Il file **Maplogic.js** è stato commentato in dettaglio, poiché ci sono alcune situazioni in cui era necessario forzare il comportamento di Leaflet per sovrascrivere regole personalizzate (come marker rossi e percorsi con il colore del **Politecnico di Bari**).
- Le librerie sono importate dal web, ma potrebbe essere più efficiente scaricarle localmente su un server del Politecnico. Non essendo particolarmente esperto nello sviluppo web, non posso dire quale soluzione sarebbe la migliore per ottimizzare il caricamento.

## Possibili sviluppi futuri per mappare l'intero Politecnico

A mio parere, ci sono due opzioni per mappare l'intero Politecnico:

1.  **Utilizzare le piantine CAD del Politecnico**: queste potrebbero essere aggiunte come layer personalizzati su OpenStreetMap usando Leaflet.
2.  **Estrarre i dati GeoJSON dall'applicazione BefreeCampus**: fare un porting dell'app in chiave web, possibilmente come webapp o usando soluzioni come Flutter/React Native per renderla disponibile su più dispositivi.

Entrambe le opzioni offrono vantaggi e svantaggi. La scelta di estrarre i dati GeoJSON e mappare il Politecnico tramite codice offre grande modularità e facilità nel cambiare la posizione delle risorse (ad esempio, se gli uffici vengono spostati, non è necessario richiedere una nuova piantina, basta cambiare il codice). D'altra parte, implementare la mappa usando le piantine offre maggiore visibilità sugli accessi, come scale e ascensori, e consentirebbe di inserire risorse in un contesto dettagliato.

Entrambe le soluzioni permetterebbero di mappare ogni piano e migliorare il riferimento delle risorse, sia in termini di accessibilità che di supporto agli utenti esterni e interni nella ricerca delle strutture.

La combinazione di Leaflet e OpenStreetMap fornisce un framework solido per entrambe le soluzioni.

## Contatti

Per qualsiasi richiesta di informazioni, [inviami una email](email:adolfocolavito@hotmail.it).
"""
    
    # Crea le cartelle se non esistono
    Path("content/it").mkdir(parents=True, exist_ok=True)
    Path("content/en").mkdir(parents=True, exist_ok=True)
    
    # Scrivi il file di esempio
    with open("content/it/example.md", "w", encoding="utf-8") as f:
        f.write(example_it_content)

    process("content/it", "content/en", "italian", "english")
    print("\nAvvio traduzione da inglese a italiano (non ci sono file di esempio in inglese, verrà saltato)...")
    process("content/en", "content/it", "english", "italian")