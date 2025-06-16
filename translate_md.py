import os
from pathlib import Path
from deep_translator import GoogleTranslator
import yaml
import re

MAX_CHARS = 4999

# Dizionario di termini da proteggere/sostituire.
# Le chiavi sono i termini come appaiono nella lingua SORGENTE (italiano).
# I valori sono la forma DESIDERATA nella lingua TARGET (inglese).
# Ho aggiunto e raffinato molti termini basandomi sul tuo articolo.
PROTECTED_TERMS_MAP = {
    "Leaflet": "Leaflet",
    "OpenStreetMap": "OpenStreetMap",
    "JavaScript": "JavaScript",
    "GeoJSON": "GeoJSON",
    "BeFreeCampus": "BeFreeCampus", # Ho corretto il tuo input in BeFreeCampus
    "HTML": "HTML",
    "CSS": "CSS",
    "JS": "JS",
    "Dataset": "Dataset", # Mantenuto maiuscolo come nel tuo input
    "Script": "Script",   # Mantenuto maiuscolo
    "Style": "Style",     # Mantenuto maiuscolo
    "SBAMappe": "SBAMappe", # Mantenuto maiuscolo
    "MapLogic.js": "MapLogic.js",
    "SBACSS": "SBACSS", # Ho corretto il tuo input in SBACSS
    "Politecnico di Bari": "Polytechnic University of Bari",
    "biblioteche di Ateneo": "university libraries", # Traduzione specifica
    "funzione costruttore": "constructor function",
    "costruttore di mappa": "map constructor", # Varianti della stessa idea
    "toggolare il menu": "toggle the menu", # Forma più comune
    "librerie": "libraries", # Per evitare "bookcases"
    "piantine": "floor plans",
    "API di Google Maps": "Google Maps APIs",
    "WebApp": "WebApp", # Mantenuto così
    "Flutter": "Flutter",
    "React Native": "React Native",
    "Screenshot_2025-06-10_alle_12.46.47_hqonwp.png": "Screenshot_2025-06-10_alle_12.46.47_hqonwp.png", # Esempio di filename
    # Esempi di link o strutture che potrebbero essere tradotte male:
    "[Inviami un'email](mailto:adolfocolavito@hotmail.it)": "[Send me an email](mailto:adolfocolavito@hotmail.it)",
    "https://mappegeneral.netlify.app": "https://mappegeneral.netlify.app",
    "https://res.cloudinary.com/dkkvkj82k/image/upload/v1749552452/Screenshot_2025-06-10_alle_12.46.47_hqonwp.png": "https://res.cloudinary.com/dkkvkj82k/image/upload/v1749552452/Screenshot_2025-06-10_alle_12.46.47_hqonwp.png",
}


def extract_front_matter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        body = parts[2].lstrip("\n")
        return fm, body
    return {}, text

def split_text(text, max_chars=MAX_CHARS):
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for p in paragraphs:
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
    # Usiamo prefissi e suffissi molto specifici per ridurre la probabilità di traduzione.
    # Invece di __HTML_0__, usiamo un pattern più "non-word-like".
    # I placeholder saranno del tipo @@HTML_0@@, @@CODE_0@@, @@TERM_0@@
    code_block_placeholders = {}
    html_placeholders = {}
    term_placeholders = {}

    text_to_process = text

    # Ordine di pre-processing: Blocchi di codice, poi HTML, poi termini specifici.

    # 1. Nasconde i blocchi di codice Markdown (```lang ... ```)
    fenced_code_block_pattern = r"(```[a-zA-Z0-9]*\n[\s\S]*?\n```)"
    def replace_fenced_code_with_placeholder(match):
        code_block = match.group(0)
        placeholder = f"@@CODE_{len(code_block_placeholders)}@@"
        code_block_placeholders[placeholder] = code_block
        return placeholder
    text_to_process = re.sub(fenced_code_block_pattern, replace_fenced_code_with_placeholder, text_to_process)

    # 2. Nasconde i tag HTML (<tag attributi>)
    # Cattura `<tag>`, `<tag/>`, `<tag ...>`, `<tag ... />`
    html_tag_pattern = r"<[^>]+>"
    def replace_html_with_placeholder(match):
        tag = match.group(0)
        placeholder = f"@@HTML_{len(html_placeholders)}@@"
        html_placeholders[placeholder] = tag
        return placeholder
    text_to_process = re.sub(html_tag_pattern, replace_html_with_placeholder, text_to_process, flags=re.IGNORECASE)

    # 3. Nasconde i termini specifici dal PROTECTED_TERMS_MAP
    # Ordina i termini per lunghezza decrescente per evitare match parziali.
    sorted_terms = sorted(PROTECTED_TERMS_MAP.keys(), key=len, reverse=True)
    for term_src in sorted_terms:
        # Se è un link Markdown o un URL completo, fai un escape semplice e non usare \b
        # Altrimenti, usa \b per matchare parole intere
        if term_src.startswith("[") or term_src.startswith("http"):
             pattern = re.escape(term_src)
        else:
             pattern = r"\b" + re.escape(term_src) + r"\b"
            
        def replace_term_with_placeholder(match):
            placeholder = f"@@TERM_{len(term_placeholders)}@@"
            term_placeholders[placeholder] = PROTECTED_TERMS_MAP[term_src]
            return placeholder
        
        # Usa re.sub con count=1 in un loop per sostituire tutte le occorrenze senza sovrapposizioni.
        # Questo è cruciale per la gestione di più occorrenze dello stesso termine.
        while re.search(pattern, text_to_process, flags=re.IGNORECASE): # re.IGNORECASE per matchare "leaflet" o "Leaflet"
            text_to_process = re.sub(pattern, replace_term_with_placeholder, text_to_process, 1, flags=re.IGNORECASE)

    # Traduce il testo rimanente
    parts = split_text(text_to_process)
    translated_parts = []
    for part in parts:
        translated_parts.append(GoogleTranslator(source=src, target=tgt).translate(part))
    translated_text = "\n\n".join(translated_parts)

    # --- Post-processamento: Ripristina nell'ordine inverso rispetto al pre-processing ---

    # 1. Ripristina i termini specifici
    sorted_placeholders = sorted(term_placeholders.keys(), key=len, reverse=True)
    for placeholder in sorted_placeholders:
        translated_text = translated_text.replace(placeholder, term_placeholders[placeholder])
        
    # 2. Ripristina i tag HTML
    for placeholder, original_tag in html_placeholders.items():
        translated_text = translated_text.replace(placeholder, original_tag)

    # 3. Ripristina i blocchi di codice
    for placeholder, original_code_block in code_block_placeholders.items():
        translated_text = translated_text.replace(placeholder, original_code_block)
        
    # Correzioni finali di formattazione Markdown e punteggiatura
    translated_text = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', translated_text)
    translated_text = re.sub(r'\*\s*(.*?)\s*\*', r'*\1*', translated_text)
    translated_text = re.sub(r'(\*\*|\*)\s*(\w+)\s*(\*\*|\*)', r'\1\2\3', translated_text)
    translated_text = re.sub(r'\s+([.,!?;:])', r'\1', translated_text)

    # Correzioni specifiche per link Markdown dove il testo è stato tradotto ma il link no
    # Questo cerca un pattern [tradotto](link originale) e assicura che il link resti invariato
    # Es: [Send me an email] (mailto:...)
    translated_text = re.sub(r'\]\s*\(', r'](', translated_text) # Rimuove spazio tra ] e (
    translated_text = re.sub(r'\s*\)\s*', r')', translated_text) # Rimuove spazi prima e dopo )

    return translated_text

def process(src_dir, tgt_dir, src_lang, tgt_lang):
    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir)
        tgt = Path(tgt_dir) / rel
        if tgt.exists():
            continue

        text = src.read_text(encoding="utf-8")
        fm, body = extract_front_matter(text)

        translated_fm = {}
        for key, value in fm.items():
            if isinstance(value, str):
                try:
                    # Gestisci i termini protetti anche nel front matter
                    processed_value = value
                    for term_src in sorted(PROTECTED_TERMS_MAP.keys(), key=len, reverse=True):
                        # Per il front matter, una semplice sostituzione funziona bene
                        # senza l'uso di placeholder complessi, dato il contesto più controllato.
                        if term_src in processed_value:
                            processed_value = processed_value.replace(term_src, PROTECTED_TERMS_MAP[term_src])
                    
                    translated_value = GoogleTranslator(source=src_lang, target=tgt_lang).translate(processed_value)
                    
                    # Applica correzioni grassetto/corsivo e punteggiatura anche al front matter
                    translated_value = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', translated_value)
                    translated_value = re.sub(r'\*\s*(.*?)\s*\*', r'*\1*', translated_value)
                    translated_value = re.sub(r'(\*\*|\*)\s*(\w+)\s*(\*\*|\*)', r'\1\2\3', translated_value)
                    translated_value = re.sub(r'\s+([.,!?;:])', r'\1', translated_value)
                    translated_fm[key] = translated_value
                except Exception as e:
                    print(f"Errore durante la traduzione del front matter per '{key}': {e}")
                    translated_fm[key] = value
            else:
                translated_fm[key] = value

        trans_body = translate(body, src_lang, tgt_lang)

        if tgt_lang.lower() == "english":
            translation_note = "> ⚠️ *This content was automatically translated from Italian using a machine translation tool.*\n\n"
        elif tgt_lang.lower() == "italian":
            translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente dall’inglese tramite un sistema di traduzione automatica.*\n\n"
        else:
            translation_note = "> ⚠️ *This content was automatically translated.*\n\n"

        content = (
            "---\n"
            + yaml.dump(translated_fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
            + "---\n\n"
            + translation_note
            + trans_body
        )

        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.write_text(content, encoding="utf-8")
        print(f"Tradotto {rel} da {src_lang} a {tgt_lang}")