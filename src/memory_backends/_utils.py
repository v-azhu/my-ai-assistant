from typing import Dict, List


def normalize_mem0_results(raw) -> List[Dict]:
    """
    Mem0's search()/get_all() have returned slightly different shapes
    across versions: sometimes a plain list of memory dicts, sometimes
    a dict like {"results": [...]}. Each memory item's text has also
    been seen under either "memory" or "content". This function
    normalizes any of those into a plain list of {"content": str}.

    If Mem0's actual response shape doesn't match what's handled here,
    this will return an empty list rather than raising — check
    https://docs.mem0.ai for the version you have installed and adjust
    the extraction below if memories aren't showing up.
    """
    if isinstance(raw, dict):
        items = raw.get("results", [])
    elif isinstance(raw, list):
        items = raw
    else:
        items = []

    normalized = []
    for item in items:
        if isinstance(item, dict):
            text = item.get("memory") or item.get("content") or item.get("text")
        else:
            text = str(item)

        if text:
            normalized.append({"content": text})

    return normalized
