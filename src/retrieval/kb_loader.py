from pathlib import Path
import re


def load_kb_chunks(kb_dir: str = "knowledge-base") -> list[dict]:
    """
    Load Markdown knowledge-base documents and create
    retrieval-friendly chunks with heading metadata.
    """

    kb_path = Path(kb_dir)
    chunks = []

    for file_path in sorted(kb_path.rglob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        # First split on the horizontal-rule boundaries
        # recommended in the assignment.
        major_sections = re.split(r"\n---\s*\n", text)

        for major_section in major_sections:
            major_section = major_section.strip()

            if not major_section:
                continue

            # Split further at Markdown headings.
            parts = re.split(
                r"(?=^#{2,3}\s+.+$)",
                major_section,
                flags=re.MULTILINE,
            )

            for part in parts:
                part = part.strip()

                if not part:
                    continue

                headings = re.findall(
                    r"^(#{1,6})\s+(.+)$",
                    part,
                    re.MULTILINE,
                )

                if headings:
                    level, heading = headings[-1]
                    heading = heading.strip()
                else:
                    heading = file_path.stem

                chunks.append(
                    {
                        "text": part,
                        "source": str(file_path),
                        "section": heading,
                        "document_type": file_path.parent.name,
                    }
                )

    return chunks