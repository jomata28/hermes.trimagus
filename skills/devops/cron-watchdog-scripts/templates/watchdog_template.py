#!/usr/bin/env python3
"""Watchdog template — STDLIB ONLY (cron runs system python, not your venv).

Contract: prints alerts to stdout only when something is actionable.
Empty stdout = silent (no Telegram message). Copy and adapt.
"""
import json, os, urllib.request, urllib.error, time

STATE_DIR = os.path.expanduser("~/.hermes/<job>_state")
CACHE_FILE = os.path.join(STATE_DIR, "cache.json")
ALERTED_FILE = os.path.join(STATE_DIR, "alerted.json")
os.makedirs(STATE_DIR, exist_ok=True)

GRACE_POLLS = 2          # consecutive misses before alerting "vanished"
MIN_CHANGE = 30          # threshold for change alerts (units depend on domain)


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return default


def fetch_source():
    """Return (items, status). status in {'OK','AUTH_ERROR','ERROR'}.
    Never raise — catch and return status so the caller can decide."""
    try:
        req = urllib.request.Request("https://api.example.com/data", headers={
            "Authorization": "Bearer " + open(os.path.expanduser("~/.hermes/<job>_token")).read().strip(),
        })
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        return data.get("data", []), "OK"
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return [], "AUTH_ERROR"
        return [], "ERROR"
    except Exception:
        return [], "ERROR"


def main():
    cache = load_json(CACHE_FILE, {})
    alerted = set(load_json(ALERTED_FILE, []))
    today = time.strftime("%Y-%m-%d")
    new_cache, alerts = {}, []

    items, status = fetch_source()
    if status == "AUTH_ERROR":
        key = f"TOKEN_EXPIRED_{today}"
        if key not in alerted:
            print("🔑 Token expired — refresh: paste new token to Hermes")
            alerted.add(key)
    elif status == "OK":
        for item in items:
            k = item["id"]
            new_cache[k] = item
            prev = cache.get(k)
            if prev is None:
                continue
            # Example: numeric change above threshold
            if abs(item.get("value", 0) - prev.get("value", 0)) >= MIN_CHANGE:
                ak = f"CHG_{k}_{item.get('value')}"
                if ak not in alerted:
                    alerts.append(f"🔔 Change: {k} → {item.get('value')}")
                    alerted.add(ak)
        # Example: vanished items with grace period
        for k, prev in cache.items():
            if k in new_cache:
                continue
            misses = prev.get("missing_polls", 0) + 1
            if misses >= GRACE_POLLS:
                ak = f"GONE_{k}"
                if ak not in alerted:
                    alerts.append(f"❌ Vanished: {k}")
                    alerted.add(ak)
            new_cache[k] = {**prev, "missing_polls": misses}
        # else: transient error → skip silently this poll (grace handles it)

    with open(CACHE_FILE, "w") as f:
        json.dump(new_cache, f)
    if len(alerted) > 2000:
        alerted = set(list(alerted)[-1000:])
    with open(ALERTED_FILE, "w") as f:
        json.dump(list(alerted), f)

    for a in alerts:
        print(a)
    # No alerts → no output → no Telegram message


if __name__ == "__main__":
    main()
