"""
Single source of truth for all keyword configuration.
All scrapers import from here — never define keywords inline.
"""

KEYWORDS: dict[str, dict[str, str]] = {
    "ea": {
        "label":    "Executive / Virtual Assistant",
        "google":   '"executive assistant" OR "virtual assistant"',
        "linkedin": "executive assistant",
        "indeed":   "executive assistant",
    },
    "social": {
        "label":    "Social Media Manager",
        "google":   '"social media manager" OR "content manager"',
        "linkedin": "social media manager",
        "indeed":   "social media manager",
    },
    "bdr": {
        "label":    "Business Development",
        "google":   '"business development representative" OR "business development manager"',
        "linkedin": "business development representative",
        "indeed":   "business development representative",
    },
    "sales": {
        "label":    "Sales / Account Executive",
        "google":   '"sales representative" OR "account executive" OR "sales manager"',
        "linkedin": "account executive",
        "indeed":   "sales representative",
    },
    "video": {
        "label":    "Video Editor / Content Creator",
        "google":   '"video editor" OR "content creator"',
        "linkedin": "video editor",
        "indeed":   "video editor",
    },
}

# Intent weight for lead scoring (higher = stronger buying signal for Jarvis)
KEYWORD_INTENT_WEIGHT: dict[str, int] = {
    "ea":     15,   # strongest signal: owner needs day-to-day ops help
    "bdr":    12,   # strong: revenue-focused, has budget
    "sales":  10,   # strong: growing, has budget
    "social": 7,    # medium: content-focused, might be solopreneur
    "video":  5,    # lower: could be agency, creative shop, not always SMB owner
}

CATEGORIES = list(KEYWORDS.keys())
