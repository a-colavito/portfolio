import os
import re
import uuid # Importa il modulo uuid
from pathlib import Path
from deep_translator import GoogleTranslator
import yaml

MAX_CHARS = 4999 # Il limite di Google Translate è 5000, meglio stare al sicuro

# Lista di termini che non dovrebbero MAI essere tradotti
FROZEN_TERMS = [
    "OpenStreetMap", "Leaflet", "SBAMappe", "MapLogic.js", "SBACSS", "GeoJSON",
    "BeFreeCampus", "CAD", "Flutter", "React Native", "Google Maps", "API",
    "Politecnico di Bari", "Poliba", "Ateneo"
]

def extract_front_matter(text):
    """Estrae il front matter (intestazione YAML) dal contenuto Markdown."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) > 2: # Assicurati che ci siano almeno due '---'
            fm = yaml.safe_load(parts[1])
            body = parts[2].lstrip("\n")
            return fm, body
    return {}, text # Ritorna un front matter vuoto e l'intero testo come body se non c'è front matter

def split_text(text, max_chars=MAX_CHARS):
    """Divide il testo in blocchi più piccoli rispettando i paragrafi."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for p in paragraphs:
        # Se l'aggiunta del paragrafo corrente (più due newline) non supera il limite
        # o se è il primo paragrafo, aggiungilo al chunk corrente.
        if len(current) + len(p) + 2 < max_chars or not current:
            current += p + "\n\n"
        else:
            # Se il chunk corrente non è vuoto, aggiungilo ai chunks e inizia un nuovo chunk
            if current:
                chunks.append(current.strip())
            current = p + "\n\n"

    if current:
        chunks.append(current.strip())

    return chunks

def protect_and_translate(text, src_lang, tgt_lang):
    """
    Protegge URLs, HTML tags, link Markdown, inline formatting e termini specifici dalla traduzione,
    quindi traduce il testo e ripristina gli elementi protetti.
    """
    protected_map = {}
    placeholder_idx = 0

    def generate_placeholder(original_content):
        nonlocal placeholder_idx
        # Usiamo un formato estremamente unico con caratteri speciali improbabili da tradurre
        placeholder = f"@@@PROTECTED_ITEM__{placeholder_idx}__$${uuid.uuid4().hex}@@@"
        protected_map[placeholder] = original_content
        placeholder_idx += 1
        return placeholder

    # L'ordine delle operazioni è importante: prima i pattern più specifici/annidati

    # 1. Proteggi i tag HTML completi (es. <img ...>, <a ...>).
    # Questo è essenziale per preservare attributi come 'src', 'style', 'href', ecc.
    # Uso .+? (non-greedy) per assicurare che corrisponda al tag più vicino e non a più tag.
    text = re.sub(r'<.+?>', lambda m: generate_placeholder(m.group(0)), text)

    # 2. Proteggi il formato Markdown inline (bold, italic, strikethrough)
    # Questi spesso causano problemi di spaziatura e capitalizzazione.
    # Uso un pattern più inclusivo per catturare la formattazione inline
    # per evitare che gli asterischi/underscore vengano trattati come parole separate.
    # ( bold **...** | italic *...* | italic _..._ | strikethrough ~~...~~ )
    text = re.sub(r'(\*\*.*?\*\*|\*.*?\*|_.*?_|~~.*?~~)', lambda m: generate_placeholder(m.group(0)), text)

    # 3. Proteggi i link e le immagini Markdown (es. ![alt](url), [testo](url))
    # Questo include le URL al loro interno.
    text = re.sub(r'(!?\[.*?\]\s*\([^\s)]*\s*\))', lambda m: generate_placeholder(m.group(0)), text)

    # 4. Proteggi i link mailto:
    text = re.sub(r'\b(mailto:[^\s)]+)\b', lambda m: generate_placeholder(m.group(0)), text)

    # 5. Proteggi i termini "congelati" specifici (es. nomi propri, termini tecnici).
    # Ordina per lunghezza decrescente per garantire che i termini più lunghi vengano
    # abbinati prima dei loro sottostringhe (es. "Google Maps" prima di "Google").
    for term in sorted(FROZEN_TERMS, key=len, reverse=True):
        # Utilizzo re.escape per gestire caratteri speciali nel termine.
        # Ho ripristinato l'uso di \b (limiti di parola) per evitare sostituzioni parziali di parole.
        # Questo è un compromesso: se un termine è "SBACSS" e appare in "SBACSS.js", \b non lo catturerà.
        # Se è necessario catturare "SBACSS" in "SBACSS.js", dovremmo rimuovere \b ma fare attenzione ai falsi positivi.
        # Per ora, manteniamo \b per prevenire la corruzione di parole.
        text = re.sub(r'\b' + re.escape(term) + r'\b', lambda m: generate_placeholder(m.group(0)), text, flags=re.IGNORECASE)

    # Traduci il testo con i placeholder
    translated_text = ""
    parts = split_text(text)
    for part in parts:
        try:
            translated_part = GoogleTranslator(source=src_lang, target=tgt_lang).translate(part)
            translated_text += translated_part + "\n\n"
        except Exception as e:
            print(f"Errore durante la traduzione di un blocco di testo: {e}")
            translated_text += part + "\n\n" # Usa la parte originale in caso di errore

    translated_text = translated_text.strip()

    # Ripristina gli elementi protetti
    # Ordina i placeholder per l'indice numerico decrescente per un ripristino sicuro
    # Il controllo `isdigit()` previene `ValueError`. `x.split('__')[1]` ora è l'indice numerico.
    # L'indice numerico si trova tra il primo e il secondo `__` nel nuovo formato `@@@PROTECTED_ITEM__{idx}__$${uuid}@@@`
    for placeholder in sorted(protected_map.keys(),
                              key=lambda x: int(x.split('__')[1]) if len(x.split('__')) > 1 and x.split('__')[1].isdigit() else -1,
                              reverse=True):
        original_content = protected_map[placeholder]
        translated_text = translated_text.replace(placeholder, original_content)

    return translated_text

def process(src_dir, tgt_dir, src_lang, tgt_lang):
    """Processa tutti i file Markdown da una cartella sorgente a una di destinazione."""
    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir)
        tgt = Path(tgt_dir) / rel
        # Salta se il file di destinazione esiste già (per evitare di ritradurre file esistenti)
        # Questo comportamento può essere modificato se si desidera forzare la ritraduzione
        if tgt.exists():
            print(f"File {rel} in {tgt_dir} esiste già, saltato.")
            continue

        text = src.read_text(encoding="utf-8")
        fm, body = extract_front_matter(text)

        translated_fm = {}
        for key, value in fm.items():
            if isinstance(value, str):
                # Regole specifiche per i valori del front matter:
                # NON tradurre campi che sono URL o percorsi
                if key in ["image", "link", "url", "permalink", "thumbnail"]: # Aggiungi altre chiavi URL se necessario
                    translated_fm[key] = value
                else:
                    try:
                        translated_value = GoogleTranslator(source=src_lang, target=tgt_lang).translate(value)
                        translated_fm[key] = translated_value
                    except Exception as e:
                        print(f"Errore durante la traduzione di '{key}' nel front matter: {e}")
                        translated_fm[key] = value # Usa il valore originale in caso di errore
            else:
                translated_fm[key] = value # Lascia invariato tutto il resto (es. date, booleani, numeri)

        # Traduci il body usando la nuova funzione di protezione
        trans_body = protect_and_translate(body, src_lang, tgt_lang)

        # ⚠️ Nota automatica di traduzione
        if tgt_lang.lower() == "english":
            translation_note = "> ⚠️ *This content was automatically translated from Italian using a machine translation tool.*\n\n"
        elif tgt_lang.lower() == "italian":
            translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente dall’inglese tramite un sistema di traduzione automatica.*\n\n"
        else:
            translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente.*\n\n"

        content = (
            "---\n"
            + yaml.dump(translated_fm, allow_unicode=True, sort_keys=False) # sort_keys=False per preservare l'ordine delle chiavi
            + "---\n\n"
            + translation_note
            + trans_body
        )

        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.write_text(content, encoding="utf-8")
        print(f"Tradotto {rel} da {src_lang} a {tgt_lang}")

if __name__ == "__main__":
    # Assicurati che le directory di input/output esistano
    Path("content/en").mkdir(parents=True, exist_ok=True)
    Path("content/it").mkdir(parents=True, exist_ok=True)

    print("Inizio traduzione da Italiano a Inglese...")
    process("content/it", "content/en", "italian", "english")
    print("\nInizio traduzione da Inglese a Italiano...")
    process("content/en", "content/it", "english", "italian")
    print("\nTraduzione completata.")
