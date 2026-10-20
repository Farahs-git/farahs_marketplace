# PreTurn governance hook.
#
# Checks the user's latest prompt against the RULES below and blocks the turn
# if any rule is violated. Input arrives as JSON on stdin; output is JSON on
# stdout. Any unexpected error returns {} (fail open).
import json
import sys

# ---------------------------------------------------------------------------
# GOVERNANCE RULES - edit this list.
#
# Each rule is a dict:
#   id       Short name (for your own reference).
#   enabled  True/False. Set False to turn a rule off without deleting it.
#   type     One of:
#              "block_word_length_at_least"  value = number
#                  Block if any word has this many characters or more.
#              "blocked_terms"               value = list of strings
#                  Block if the prompt contains any term (case-insensitive).
#              "max_prompt_chars"            value = number
#                  Block if the prompt is longer than this many characters.
#   value    The setting for the rule type (see above).
#   message  Text shown to the user when the rule blocks the turn.
# ---------------------------------------------------------------------------
RULES = [
    {
        "id": "no-long-words",
        "enabled": True,
        "type": "block_word_length_at_least",
        "value": 10,
        "message": "Blocked by governance: prompts may not contain words of 8 or more characters.",
    },
    {
        "id": "no-restricted-terms",
        "enabled": True,
        "type": "blocked_terms",
        "value": ["password", "secret"],
        "message": "Blocked by governance: the prompt contains a restricted term.",
    },
    {
        "id": "short-prompts-only",
        "enabled": False,
        "type": "max_prompt_chars",
        "value": 2000,
        "message": "Blocked by governance: prompts are limited to 2000 characters.",
    },
]
# ---------------------------------------------------------------------------


def _to_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for k in ("content", "text", "message"):
            if k in value:
                return _to_text(value[k])
        return ""
    if isinstance(value, list):
        return " ".join(_to_text(v) for v in value)
    return ""


def get_prompt(hook_input):
    """PreTurnInput = {turn_id, messages, run_context}. Use the last user message."""
    messages = hook_input.get("messages")
    if isinstance(messages, list):
        for msg in reversed(messages):
            if isinstance(msg, dict) and msg.get("role") == "user":
                text = _to_text(msg.get("content"))
                if text:
                    return text
    return ""


def words(text):
    """Split text into runs of letters/digits."""
    out = []
    cur = []
    for ch in text:
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            out.append("".join(cur))
            cur = []
    if cur:
        out.append("".join(cur))
    return out


def evaluate(rule, prompt):
    """Return the rule's message if the prompt violates it, else None."""
    if not rule.get("enabled", True):
        return None
    rtype = rule.get("type")
    value = rule.get("value")
    msg = rule.get("message") or "Blocked by governance rule: %s" % rule.get("id", rtype)

    if rtype == "block_word_length_at_least":
        if any(len(w) >= value for w in words(prompt)):
            return msg
    elif rtype == "blocked_terms":
        lowered = prompt.lower()
        if any(t.lower() in lowered for t in value):
            return msg
    elif rtype == "max_prompt_chars":
        if len(prompt) > value:
            return msg
    return None


def main():
    hook_input = json.loads(sys.stdin.read() or "{}")
    prompt = get_prompt(hook_input)
    if not prompt:
        return {}
    for rule in RULES:
        try:
            violation = evaluate(rule, prompt)
        except Exception:
            continue  # a bad rule never blocks the user
        if violation:
            return {"block": True, "block_reason": violation}
    return {}


try:
    print(json.dumps(main()))
except Exception:
    print("{}")
