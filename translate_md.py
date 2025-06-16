import os
from pathlib import Path
import yaml
# Importa la classe principale dal modulo
from md_translate import Translator
# Potresti aver bisogno di configurare un provider, es. per Google Cloud Translation API
# from md_translate.backends import GoogleTranslateBackend

def process_with_md_translate(src_dir, tgt_dir, src_lang_code, tgt_lang_code):
    # Inizializza il traduttore. Potresti voler configurare un backend specifico
    # se non vuoi usare il default (spesso Google Translate via web, come deep_translator)
    # Per una qualità e affidabilità migliori, useresti un backend API configurato.
    # Ad esempio: translator = Translator(backend=GoogleTranslateBackend(api_key="TUA_CHIAVE_API"))
    
    # Se vuoi usare il default (Google Translate web scraping, come deep_translator senza key)
    translator = Translator() 

    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir)
        tgt = Path(tgt_dir) / rel
        
        # Puoi aggiungere qui il controllo `if tgt.exists(): continue` se vuoi saltare i file già tradotti.

        try:
            # md_translate gestisce la lettura, estrazione del front matter,
            # protezione di codice/HTML/link e traduzione.
            # I codici lingua devono essere in formato ISO (es. 'it', 'en').
            translated_content = translator.translate_markdown(
                src.read_text(encoding="utf-8"), 
                source_language=src_lang_code, 
                target_language=tgt_lang_code
            )

            # md_translate gestisce già la riscrittura del front matter e del corpo.
            # Dovresti solo aggiungere la tua nota di traduzione se vuoi.
            fm, body = extract_front_matter(translated_content) # Estrai di nuovo per inserire la nota
            
            translation_note = ""
            if tgt_lang_code.lower() == "en":
                translation_note = "> ⚠️ *This content was automatically translated from Italian using a machine translation tool.*\n\n"
            elif tgt_lang_code.lower() == "it":
                translation_note = "> ⚠️ *Questo contenuto è stato tradotto automaticamente dall’inglese tramite un sistema di traduzione automatica.*\n\n"
            else:
                translation_note = "> ⚠️ *This content was automatically translated.*\n\n"

            final_content = (
                "---\n"
                + yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
                + "---\n\n"
                + translation_note # Aggiungi la nota dopo il front matter
                + body
            )

            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_text(final_content, encoding="utf-8")
            print(f"Tradotto {rel} da {src_lang_code} a {tgt_lang_code} con md_translate")

        except Exception as e:
            print(f"Errore durante la traduzione di {src} con md_translate: {e}")

# Esempio di chiamata (dovresti mappare le tue stringhe "italian", "english" a 'it', 'en')
# process_with_md_translate("content/it", "content/en", "it", "en")