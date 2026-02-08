import re
import json
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

PROFILE = 'https://tryhackme.com/p/william.l.munoz'
REPO_ROOT = Path(__file__).resolve().parents[2]
README = REPO_ROOT / 'README.md'
STATE = REPO_ROOT / '.thm_state.json'


def fetch_profile_html():
    r = requests.get(PROFILE, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
    r.raise_for_status()
    return r.text


def parse_badges(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(" ")
    out = []
    # Known Linux badge to ensure we track it
    if 'cat linux.txt' in text.lower():
        out.append('Linux Fundamentals (cat linux.txt)')
    # Fallback: extract any phrase ending in '.txt' around 'linux'
    m = re.findall(r'([A-Za-z0-9 ._-]{3,30}linux\.txt)', text, flags=re.I)
    out.extend(m)
    # Dedup and tidy
    cleaned = []
    seen = set()
    for b in out:
        bb = b.strip()
        if bb.lower() not in seen:
            seen.add(bb.lower())
            cleaned.append(bb)
    return cleaned


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            return {"badges": []}
    return {"badges": []}


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2))


def append_hands_on_section(badge_name):
    today = datetime.utcnow().date().isoformat()
    entry = f"- TryHackMe: {badge_name} — Completed {today}"
    md = README.read_text()
    if '## Hands-on Labs' not in md:
        md += '\n\n## Hands-on Labs\n\n'
    # Avoid duplicate lines
    if entry in md:
        return False
    # Insert at top of section after header
    parts = md.split('## Hands-on Labs')
    if len(parts) == 2:
        head, tail = parts
        tail_lines = tail.splitlines()
        new_tail = '\n'.join(['## Hands-on Labs', entry] + tail_lines[1:])
        new_md = head + new_tail
    else:
        new_md = md + f"\n{entry}\n"
    README.write_text(new_md)
    return True


def main():
    html = fetch_profile_html()
    badges = parse_badges(html)
    state = load_state()
    known = set(state.get('badges', []))
    new_badges = [b for b in badges if b not in known]
    changed = False
    for b in new_badges:
        changed |= append_hands_on_section(b)
    if new_badges:
        state['badges'] = sorted(known | set(new_badges))
        save_state(state)
    if not changed:
        print('No updates')

if __name__ == '__main__':
    main()
