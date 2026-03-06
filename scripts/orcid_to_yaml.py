import json
import urllib.request
from pathlib import Path

ORCID = "0000-0001-5149-5670"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def safe_get(d, *keys, default=""):
    cur = d
    for k in keys:
        if cur is None:
            return default
        cur = cur.get(k)
    return cur if cur is not None else default


def format_authors(contributors):
    authors = []

    for c in contributors:
        name = c.get("credit-name", {}).get("value", "")

        if not name:
            continue

        name = name.strip()

        # If ORCID already returns "Lastname, Initials"
        if "," in name:
            authors.append(name)
            continue

        parts = name.split()

        if len(parts) == 1:
            authors.append(parts[0])
            continue

        last = parts[-1]
        initials = " ".join([p[0] + "." for p in parts[:-1]])

        authors.append(f"{last}, {initials}")

    return ", ".join(authors)


def extract_doi(external_ids):
    for ext in external_ids:
        if ext.get("external-id-type") == "doi":
            return ext.get("external-id-value", "")
    return ""


works_data = fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/works")
publications = []

for group in works_data.get("group", []):
    summaries = group.get("work-summary", [])
    if not summaries:
        continue

    summary = summaries[0]

    if summary.get("type") != "journal-article":
        continue

    put_code = summary.get("put-code")
    if not put_code:
        continue

    work = fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/work/{put_code}")

    title = safe_get(work, "title", "title", "value", default="")
    subtitle = safe_get(work, "title", "subtitle", "value", default="")
    if subtitle:
        title = f"{title}: {subtitle}"

    year = safe_get(work, "publication-date", "year", "value", default="")
    month = safe_get(work, "publication-date", "month", "value", default="")
    day = safe_get(work, "publication-date", "day", "value", default="")

    journal = safe_get(work, "journal-title", "value", default="")
    volume = safe_get(work, "journal-title", "value", default="")
    short_desc = safe_get(work, "short-description", default="")

    contributors = safe_get(work, "contributors", "contributor", default=[])
    authors = format_authors(contributors)

    external_ids = safe_get(work, "external-ids", "external-id", default=[])
    doi = extract_doi(external_ids)

    url = f"https://doi.org/{doi}" if doi else ""

    publication = {
        "title": title,
        "authors": authors,
        "year": year,
        "month": month,
        "day": day,
        "journal": journal,
        "volume": "",
        "issue": "",
        "pages": "",
        "doi": doi,
        "url": url,
        "description": short_desc,
    }

    # Try to extract volume/issue/pages from citation if present
    citation_value = safe_get(work, "citation", "citation-value", default="")

    publications.append(publication)

publications.sort(key=lambda x: x["year"], reverse=True)

out = Path("_data/publications.yml")
out.parent.mkdir(exist_ok=True)

with out.open("w", encoding="utf-8") as f:
    f.write("# Auto-generated from ORCID. Do not edit manually.\n")
    for p in publications:
        f.write("- title: " + json.dumps(p["title"], ensure_ascii=False) + "\n")
        f.write("  authors: " + json.dumps(p["authors"], ensure_ascii=False) + "\n")
        f.write("  year: " + json.dumps(p["year"], ensure_ascii=False) + "\n")
        f.write("  month: " + json.dumps(p["month"], ensure_ascii=False) + "\n")
        f.write("  day: " + json.dumps(p["day"], ensure_ascii=False) + "\n")
        f.write("  journal: " + json.dumps(p["journal"], ensure_ascii=False) + "\n")
        f.write("  volume: " + json.dumps(p["volume"], ensure_ascii=False) + "\n")
        f.write("  issue: " + json.dumps(p["issue"], ensure_ascii=False) + "\n")
        f.write("  pages: " + json.dumps(p["pages"], ensure_ascii=False) + "\n")
        f.write("  doi: " + json.dumps(p["doi"], ensure_ascii=False) + "\n")
        f.write("  url: " + json.dumps(p["url"], ensure_ascii=False) + "\n")
        f.write("  description: " + json.dumps(p["description"], ensure_ascii=False) + "\n\n")

print(f"Updated {len(publications)} journal articles.")
