import json
import urllib.request
from pathlib import Path

ORCID = "0000-0001-5149-5670"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

data = fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/works")

publications = []

for group in data["group"]:
    summary = group["work-summary"][0]
    
    if summary["type"] != "journal-article":
        continue

    title = summary["title"]["title"]["value"]

    year = ""
    try:
        year = summary["publication-date"]["year"]["value"]
    except:
        pass

    doi = ""
    for ext in summary.get("external-ids", {}).get("external-id", []):
        if ext["external-id-type"] == "doi":
            doi = ext["external-id-value"]

    publications.append({
        "title": title,
        "year": year,
        "doi": doi
    })

publications.sort(key=lambda x: x["year"], reverse=True)

out = Path("_data/publications.yml")
out.parent.mkdir(exist_ok=True)

with out.open("w") as f:
    for p in publications:
        f.write("- title: \"" + p["title"] + "\"\n")
        f.write("  year: \"" + p["year"] + "\"\n")
        f.write("  doi: \"" + p["doi"] + "\"\n\n")

print("Publications updated")
