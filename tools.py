"""Tools the CyberBond agent can call."""
import hashlib
import re
from datetime import datetime, timedelta, timezone

from langchain_core.tools import tool

from rag.retriever import retrieve


@tool
def search_notes(query: str) -> str:
    """Search the user's digital forensics course notes (chain of custody,
    file systems, investigation process, digital evidence). Use this for any
    forensics concept or theory question."""
    docs = retrieve(query)
    if not docs:
        return "No relevant notes found."
    parts = []
    for d in docs:
        name = d.metadata.get("source", "unknown").split("\\")[-1]
        page = d.metadata.get("page")
        label = f"{name} p.{page + 1}" if isinstance(page, int) else name
        parts.append(f"[{label}]\n{d.page_content}")
    return "\n\n".join(parts)


@tool
def calculate_hashes(text: str) -> str:
    """Compute MD5, SHA-1 and SHA-256 hashes of the given text."""
    data = text.encode("utf-8")
    return (
        f"MD5:     {hashlib.md5(data).hexdigest()}\n"
        f"SHA-1:   {hashlib.sha1(data).hexdigest()}\n"
        f"SHA-256: {hashlib.sha256(data).hexdigest()}"
    )


@tool
def convert_timestamp(value: str) -> str:
    """Convert a Unix epoch (seconds or milliseconds) or a Windows FILETIME
    (100-nanosecond ticks since 1601) number into a readable UTC date."""
    try:
        n = int(value.strip())
    except ValueError:
        return "Please provide a whole number."
    try:
        if n > 10**16:  # Windows FILETIME
            kind = "Windows FILETIME"
            dt = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=n // 10)
        elif n > 10**11:  # Unix milliseconds
            kind = "Unix epoch (milliseconds)"
            dt = datetime.fromtimestamp(n / 1000, tz=timezone.utc)
        else:  # Unix seconds
            kind = "Unix epoch (seconds)"
            dt = datetime.fromtimestamp(n, tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        return "That number is outside a valid date range."
    return f"Detected as {kind}: {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC"


@tool
def extract_iocs(text: str) -> str:
    """Extract indicators of compromise (IPv4 addresses, URLs, domains, email
    addresses, MD5/SHA-1/SHA-256 hashes) from pasted logs or report text."""
    patterns = {
        "IPv4": r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b",
        "URL": r"https?://[^\s\"'<>]+",
        "Email": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
        "Domain": r"\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|io|ru|cn|info|biz|xyz|in|gov|edu)\b",
        "SHA-256": r"\b[a-fA-F0-9]{64}\b",
        "SHA-1": r"\b[a-fA-F0-9]{40}\b",
        "MD5": r"\b[a-fA-F0-9]{32}\b",
    }
    lines = []
    for name, pat in patterns.items():
        found = sorted(set(re.findall(pat, text)))
        if found:
            lines.append(f"{name} ({len(found)}): " + ", ".join(found))
    return "\n".join(lines) if lines else "No IOCs found."


SIGNATURES = [
    ("PNG image", "89504E470D0A1A0A", 0),
    ("SQLite database", "53514C69746520666F726D6174", 0),
    ("Microsoft OLE2 (legacy .doc/.xls/.ppt)", "D0CF11E0A1B11AE1", 0),
    ("7-Zip archive", "377ABCAF271C", 0),
    ("RAR archive", "526172211A07", 0),
    ("PDF document", "25504446", 0),
    ("ZIP container (also .docx/.xlsx/.pptx/.jar/.apk)", "504B0304", 0),
    ("ELF executable (Linux)", "7F454C46", 0),
    ("GIF image", "47494638", 0),
    ("RTF document", "7B5C727466", 0),
    ("JPEG image", "FFD8FF", 0),
    ("MP4/MOV video", "66747970", 4),
    ("Windows executable (PE/MZ)", "4D5A", 0),
    ("MP3 audio (ID3)", "494433", 0),
    ("GZIP archive", "1F8B", 0),
    ("BMP image", "424D", 0),
]


@tool
def check_file_signature(hex_bytes: str) -> str:
    """Identify a file type from its first bytes (magic number), given as a
    hex string such as '25 50 44 46' or '89504E47'."""
    clean = re.sub(r"[^0-9A-Fa-f]", "", hex_bytes).upper()
    if len(clean) < 4:
        return "Provide at least 2 bytes of hex (e.g. 25 50 44 46)."
    for name, sig, offset in SIGNATURES:
        start = offset * 2
        if clean[start:start + len(sig)] == sig:
            return f"Matches signature for: {name}"
    return "No known signature matched. Try providing more bytes."


ALL_TOOLS = [search_notes, calculate_hashes, convert_timestamp, extract_iocs, check_file_signature]