import os
from pathlib import Path
from deep_translator import GoogleTranslator
import yaml
import re

MAX_CHARS = 4999

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
    html_placeholders = {}

    html_tag_pattern = r"<[^>]+>" 
    
    def replace_html_with_placeholder(match):
        tag = match.group(0)
        placeholder = f"__HTML_PLACEHOLDER_{len(html_placeholders)}__"
        html_placeholders[placeholder] = tag
        return placeholder

    text_preprocessed = re.sub(html_tag_pattern, replace_html_with_placeholder, text, flags=re.IGNORECASE)

    parts = split_text(text_preprocessed)
    translated_parts = []
    for part in parts:
        translated_parts.append(GoogleTranslator(source=src, target=tgt).translate(part))
    
    translated_text = "\n\n".join(translated_parts)

    for placeholder, original_tag in html_placeholders.items():
        translated_text = translated_text.replace(placeholder, original_tag)
        
    translated_text = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', translated_text)
    translated_text = re.sub(r'\*\s*(.*?)\s*\*', r'*\1*', translated_text)
    translated_text = re.sub(r'(\*\*|\*)\s*(\w+)\s*(\*\*|\*)', r'\1\2\3', translated_text)
    translated_text = re.sub(r'\s+([.,!?;:])', r'\1', translated_text)

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
                    translated_value = GoogleTranslator(source=src_lang, target=tgt_lang).translate(value)
                    translated_value = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', translated_value)
                    translated_value = re.sub(r'\*\s*(.*?)\s*\*', r'*\1*', translated_value)
                    translated_value = re.sub(r'(\*\*|\*)\s*(\w+)\s*(\*\*|\*)', r'\1\2\3', translated_value)
                    translated_value = re.sub(r'\s+([.,!?;:])', r'\1', translated_value)
                    translated_fm[key] = translated_value
                except Exception as e:
                    print(f"Errore durante la traduzione di '{key}': {e}")
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
            + yaml.dump(translated_fm, allow_unicode=True, default_flow_style=False)
            + "---\n\n"
            + translation_note
            + trans_body
        )

        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.write_text(content, encoding="utf-8")
        print(f"Tradotto {rel} da {src_lang} a {tgt_lang}")