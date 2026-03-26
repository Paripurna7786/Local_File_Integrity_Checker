import hashlib
import os


def get_hash(filename: str) -> str:
    """Return the SHA-256 hex digest of the given file."""
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def shorten_path(path: str, max_len: int = 42) -> str:
    """Shorten a long file path for display purposes."""
    if len(path) <= max_len:
        return path
    parts = path.replace("\\", "/").split("/")
    if len(parts) > 3:
        return f"…/{'/'.join(parts[-2:])}"
    return "…" + path[-(max_len - 1):]


def format_size(size_bytes: int) -> str:
    """Convert byte count to a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes:,} B"
    elif size_bytes < 1_048_576:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1_048_576:.1f} MB"


def get_file_info(filepath: str) -> dict:
    """
    Return a dict with display-ready info about the file.
    Keys: name, short_path, size_str, hash, short_hash
    """
    name       = os.path.basename(filepath)
    size_str   = format_size(os.path.getsize(filepath))
    file_hash  = get_hash(filepath)
    short_hash = file_hash[:8] + "..." + file_hash[-8:]

    return {
        "name":       name,
        "short_path": shorten_path(filepath),
        "size_str":   size_str,
        "hash":       file_hash,
        "short_hash": short_hash,
    }


def verify_integrity(filepath: str, original_hash: str) -> dict:
    """
    Compare current file hash against the original.
    Returns dict with: intact (bool), original_hash, current_hash,
    original_short, current_short.
    """
    current_hash  = get_hash(filepath)
    intact        = current_hash == original_hash
    return {
        "intact":         intact,
        "original_hash":  original_hash,
        "current_hash":   current_hash,
        "original_short": original_hash[:8] + "..." + original_hash[-8:],
        "current_short":  current_hash[:8]  + "..." + current_hash[-8:],
    }