import re
from typing import List, Dict

def chunk_text_by_heading(text: str, source: str) -> List[Dict]:
    """
    Splits document into chunks based on headings (numbered or bold-style sections).
    Each chunk contains a title and its content.
    """
    pattern = re.compile(r"(?:(?<=\n)|^)\s*(\d+[\.\)]?)\s*(.+?)(?=\n\d+[\.\)]|\Z)", re.DOTALL)

    matches = pattern.finditer(text)
    chunks = []

    for idx, match in enumerate(matches):
        heading_number = match.group(1).strip()
        title_and_content = match.group(2).strip()

        # Split into title + content
        lines = title_and_content.split("\n", 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""

        chunks.append({
            "source": source,
            "chunk_id": f"{source}_{idx}",
            "title": title,
            "content": content
        })

    return chunks
