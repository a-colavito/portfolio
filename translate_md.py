import os
from pathlib import Path
from deep_translator import GoogleTranslator
import yaml
import textwrap

MAX_CHARS = 4999  # Google Translate limit is 5000, stay safe

def extract_front_matter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        body = parts[2].lstrip("\n")
        return fm, body
    return {}, text

def split_text(text, max_chars=MAX_CHARS):
    # Mantieni paragrafi interi (non spezzare in mezzo a un paragrafo)
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) + 2 < max_chars:
            current += p + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            current = p + "\n\n"

    if current:
        chunks.append(current.strip())

    return chunks

def translate(text, src, tgt):
    parts = split_text(text)
    translated = []
    for part in parts:
        translated.append(GoogleTranslator(source=src, target=tgt).translate(part))
    return "\n\n".join(translated)

def process(src_dir, tgt_dir, src_lang, tgt_lang):
    for src in Path(src_dir).rglob("*.md"):
        rel = src.relative_to(src_dir)
        tgt = Path(tgt_dir) / rel
        if tgt.exists():
            continue

        text = src.read_text(encoding="utf-8")
        fm, body = extract_front_matter(text)

        # ✨ Traduci i valori del front matter se sono stringhe
        translated_fm = {}
        for key, value in fm.items():
            if isinstance(value, str):
                try:
                    translated_value = GoogleTranslator(source=src_lang, target=tgt_lang).translate(value)
                    translated_fm[key] = translated_value
                except Exception as e:
                    print(f"Errore durante la traduzione di '{key}': {e}")
                    translated_fm[key] = value
            else:
                translated_fm[key] = value  # Mantieni tutto il resto invariato

        trans_body = translate(body, src_lang, tgt_lang)

        content = "---\n" + yaml.dump(translated_fm, allow_unicode=True) + "---\n\n" + trans_body
        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.write_text(content, encoding="utf-8")
        print(f"Tradotto {rel} da {src_lang} a {tgt_lang}")

if __name__ == "__main__":
    process("content/it", "content/en", "italian", "english")
    process("content/en", "content/it", "english", "italian")