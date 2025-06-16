import os
from pathlib import Path
import subprocess
import yaml

def extract_front_matter(text):
    """Estrae il front matter (intestazione YAML) dal contenuto Markdown."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) > 2: # Assicurati che ci siano almeno 3 parti dopo lo split "---"
            fm = yaml.safe_load(parts[1])
            body = parts[2].lstrip("\n")
            return fm, body
    return {}, text # Ritorna un dizionario vuoto e il testo originale se non c'è front matter

def process(src_dir, tgt_dir, src_lang, tgt_lang):
    """Processa tutti i file Markdown da una cartella sorgente a una di destinazione usando md-translate CLI."""
    
    lang_map = {
        "italian": "it",
        "english": "en"
    }
    src_lang_code = lang_map.get(src_lang.lower(), src_lang.lower())
    tgt_lang_code = lang_map.get(tgt_lang.lower(), tgt_lang.lower())

    # Assicurati che la directory base di destinazione esista (es. content/en)
    Path(tgt_dir).mkdir(parents=True, exist_ok=True)
    print(f"DEBUG: Directory base di destinazione garantita: {Path(tgt_dir).absolute()}")

    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir) # Esempio: "about.md" o "subfolder/doc.md"
        tgt = Path(tgt_dir) / rel     # Esempio: "content/en/about.md" o "content/en/subfolder/doc.md"
        
        print(f"\n--- Processamento file: {src.name} ---")
        print(f"DEBUG: Percorso relativo: {rel}")
        print(f"DEBUG: Percorso di destinazione desiderato: {tgt.absolute()}")

        # Salta la traduzione se il file di destinazione esiste già
        if tgt.exists():
            print(f"DEBUG: File '{rel}' in '{tgt_dir}' esiste già, saltando.")
            continue
        
        # Crea la directory genitore per il file di destinazione, se non esiste (es. content/en/subfolder/)
        tgt.parent.mkdir(parents=True, exist_ok=True)
        print(f"DEBUG: Directory genitore per il file di destinazione garantita: {tgt.parent.absolute()}")

        # Costruisci il percorso temporaneo dove md-translate scriverà il suo output
        # Esempio: se src è "content/it/docs/my_doc.md"
        # temp_translated_src sarà "content/it/docs/my_doc_translated.md"
        temp_translated_src = src.with_stem(src.stem + "_translated")
        
        print(f"DEBUG: md-translate creerà un file temporaneo qui: {temp_translated_src.absolute()}")

        # Costruisci il comando md-translate
        command = [
            "md-translate",
            str(src.absolute()), # Passa il percorso assoluto per evitare ambiguità
            "-F", src_lang_code,
            "-T", tgt_lang_code,
            "-P", "google", # Puoi scegliere qui il servizio che preferisci
            "-N", # Crea un nuovo file con suffisso _translated.md
            "-O"  # Sovrascrive se il file _translated.md esiste già (utile per re-run)
        ]

        print(f"DEBUG: Esecuzione comando: {' '.join(command)}")
        try:
            # Esegui il comando md-translate
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("--- Output stdout di md-translate ---")
            print(result.stdout)
            if result.stderr:
                print("--- Output stderr di md-translate ---")
                print(result.stderr)
            print("--- Fine output di md-translate ---")

            # Verifica se il file temporaneo è stato effettivamente creato da md-translate
            if temp_translated_src.exists():
                print(f"DEBUG: SUCCESSO - File tradotto temporaneo '{temp_translated_src.name}' TROVATO dopo l'esecuzione di md-translate.")
                translated_text = temp_translated_src.read_text(encoding="utf-8")
                
                # Estrai il front matter e il corpo dal testo tradotto
                fm, body = extract_front_matter(translated_text)

                # Aggiungi la tua nota automatica di traduzione personalizzata
                translation_note = ""
                if tgt_lang.lower() == "english":
                    translation_note = "> ⚠️ *This content was automatically translated from Italian using a machine translation tool.*\n\n"
                elif tgt_lang.lower() == "italian":
                    translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente dall’inglese tramite un sistema di traduzione automatica.*\n\n"
                else:
                    translation_note = "> ⚠️ *This content was automatically translated.*\n\n"

                # Ricostruisci il contenuto finale del file, inclusa la nota
                final_content = (
                    "---\n"
                    + yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
                    + "---\n\n"
                    + translation_note
                    + body
                )

                # Scrivi il contenuto finale nel percorso di destinazione corretto (nella cartella 'en')
                tgt.write_text(final_content, encoding="utf-8")
                print(f"DEBUG: Contenuto tradotto finale scritto con successo in: {tgt.absolute()}")
                
                # Rimuovi il file temporaneo creato da md-translate
                temp_translated_src.unlink()
                print(f"DEBUG: File temporaneo rimosso: {temp_translated_src.absolute()}")
                print(f"Traduzione e copia completate per '{rel}' da {src_lang} a {tgt_lang}")
            else:
                print(f"ERRORE GRAVE: File tradotto temporaneo NON TROVATO a: {temp_translated_src.absolute()} dopo l'esecuzione di md-translate.")
                print("Questo indica che md-translate non ha creato il file di output atteso.")
                # Potresti voler interrompere il processo qui o gestire l'errore in modo specifico
                # raise FileNotFoundError(f"md-translate failed to create {temp_translated_src}")


        except subprocess.CalledProcessError as e:
            print(f"ERRORE: Comando md-translate fallito per {src}:")
            print(f"Comando: {e.cmd}")
            print(f"Codice di ritorno: {e.returncode}")
            print(f"Output Stdout: {e.stdout}")
            print(f"Output Stderr: {e.stderr}")
        except Exception as e:
            print(f"ERRORE GENERICO: Durante il processamento di {src}: {e}")