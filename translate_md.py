import os
from pathlib import Path
import subprocess # Modulo per eseguire comandi esterni
import yaml

# Non più necessari se usiamo la CLI di md-translate per la traduzione effettiva
# from deep_translator import GoogleTranslator
# import re
# MAX_CHARS = 4999
# PROTECTED_TERMS_MAP = {} # Questo non sarà più gestito dal tuo script, ma da md-translate

def extract_front_matter(text):
    """Estrae il front matter (intestazione YAML) dal contenuto Markdown."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) > 2: # Assicurati che ci siano almeno 3 parti dopo lo split
            fm = yaml.safe_load(parts[1])
            body = parts[2].lstrip("\n")
            return fm, body
    return {}, text # Ritorna un dizionario vuoto e il testo originale se non c'è front matter

def process(src_dir, tgt_dir, src_lang, tgt_lang):
    """Processa tutti i file Markdown da una cartella sorgente a una di destinazione usando md-translate CLI."""
    
    # Mappa i nomi delle lingue "italiano", "english" ai codici ISO richiesti da md-translate
    # (Generalmente 'it', 'en'). Puoi estendere questa mappatura se hai più lingue.
    lang_map = {
        "italian": "it",
        "english": "en"
    }
    src_lang_code = lang_map.get(src_lang.lower(), src_lang.lower()) # Usa il codice se non mappato
    tgt_lang_code = lang_map.get(tgt_lang.lower(), tgt_lang.lower())

    # Assicurati che le directory di destinazione esistano
    Path(tgt_dir).mkdir(parents=True, exist_ok=True)

    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir)
        tgt = Path(tgt_dir) / rel

        # Salta la traduzione se il file di destinazione esiste già
        # e non vogliamo sovrascriverlo. Se vuoi sempre sovrascrivere, puoi rimuovere questo blocco
        # o usare l'opzione `-O` (overwrite) di md-translate.
        if tgt.exists():
            print(f"File {rel} in {tgt_dir} esiste già, saltando.")
            continue
        
        # Crea la directory genitore per il file di destinazione, se non esiste
        tgt.parent.mkdir(parents=True, exist_ok=True)
        
        # Costruisci il comando md-translate
        # Stiamo usando l'opzione `--new-file` che crea un nuovo file con suffisso _translated
        # e poi lo rinominiamo nel percorso finale. Questo è un workaround perché md-translate
        # non ha un'opzione diretta per specificare una cartella di output diversa dall'originale.
        # Oppure, se md-translate supporta la traduzione in-place e tu gestisci la copia
        # del file nella cartella target, sarebbe ancora più semplice.
        
        # Alternativa 1: Tradurre temporaneamente e poi spostare/copiare
        # Visto che il README dice "Create a new file with translated text ... in the same directory ... with a "_translated" suffix"
        # È più facile far fare a md-translate la traduzione nella stessa directory
        # e poi spostare il file tradotto nella directory di destinazione.

        # Definisci il percorso temporaneo del file tradotto
        temp_translated_src = src.with_suffix('') # Rimuovi .md
        temp_translated_src = Path(str(temp_translated_src) + "_translated.md") # Aggiungi _translated.md

        # Il comando CLI di md-translate
        # -F: lingua sorgente
        # -T: lingua target
        # -P: servizio di traduzione (es. google, deepl, yandex, bing)
        # -N: crea un nuovo file con suffisso _translated
        # -O: sovrascrive i file già tradotti (se _translated esiste)
        # Non usiamo -D (drop-original) perché vogliamo solo il testo tradotto, non originale + tradotto
        command = [
            "md-translate",
            str(src), # Il percorso del file sorgente da tradurre
            "-F", src_lang_code,
            "-T", tgt_lang_code,
            "-P", "google", # Puoi scegliere qui il servizio che preferisci: google, bing, deepl, yandex, etc.
            "-N", # Crea un nuovo file con suffisso _translated.md
            "-O" # Sovrascrive se il file _translated.md esiste già
        ]

        print(f"Esecuzione comando: {' '.join(command)}")
        try:
            # Esegui il comando
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(result.stdout)
            if result.stderr:
                print(f"Errore stderr durante la traduzione: {result.stderr}")

            # md-translate ha creato un file come "nomefile_translated.md" nella stessa directory di src
            # Ora leggiamo quel file, aggiungiamo la nostra nota e lo spostiamo nel percorso di destinazione.

            if temp_translated_src.exists():
                translated_text = temp_translated_src.read_text(encoding="utf-8")
                
                # md-translate gestisce già la traduzione del front matter,
                # ma vogliamo estrarlo di nuovo per assicurare che la nota sia messa correttamente.
                fm, body = extract_front_matter(translated_text)

                # Aggiungi la tua nota automatica di traduzione
                translation_note = ""
                if tgt_lang.lower() == "english":
                    translation_note = "> ⚠️ *This content was automatically translated from Italian using a machine translation tool.*\n\n"
                elif tgt_lang.lower() == "italian":
                    translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente dall’inglese tramite un sistema di traduzione automatica.*\n\n"
                else:
                    translation_note = "> ⚠️ *This content was automatically translated.*\n\n"

                # Ricostruisci il contenuto per includere la nota
                final_content = (
                    "---\n"
                    + yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
                    + "---\n\n"
                    + translation_note
                    + body
                )

                tgt.write_text(final_content, encoding="utf-8")
                print(f"Tradotto e copiato {rel} da {src_lang} a {tgt_lang}")
                
                # Rimuovi il file temporaneo creato da md-translate
                temp_translated_src.unlink()
            else:
                print(f"Errore: File tradotto temporaneo non trovato: {temp_translated_src}")


        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione di md-translate per {src}:")
            print(f"Comando fallito: {e.cmd}")
            print(f"Output stdout: {e.stdout}")
            print(f"Output stderr: {e.stderr}")
        except Exception as e:
            print(f"Errore generico durante il processamento di {src}: {e}")

# Esempio di utilizzo:
# process("content/it", "content/en", "italian", "english")
# process("content/en", "content/it", "english", "italian")