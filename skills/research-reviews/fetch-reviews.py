#!/usr/bin/env python3
"""SerpAPI Google Maps Reviews Fetcher
Usage: python3 fetch-reviews.py <google_maps_url>
Output: JSON to stdout — keys: place_info, topics, reviews, total
"""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def load_api_key() -> str:
    env_path = Path.home() / ".claude" / "serpapi.env"
    if not env_path.exists():
        raise SystemExit(
            f"ERROR: {env_path} not found.\n"
            "Tạo file với nội dung: SERPAPI_KEY=your_key_here"
        )
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("SERPAPI_KEY") and "=" in line:
            return line.split("=", 1)[1].strip().strip("'\"")
    raise SystemExit("ERROR: SERPAPI_KEY không tìm thấy trong serpapi.env")


def serpapi_get(params: dict) -> dict:
    url = "https://serpapi.com/search?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"SerpAPI HTTP {e.code}: {body[:300]}")


def resolve_url(url: str) -> str:
    """Expand short URLs (maps.app.goo.gl, goo.gl)."""
    if "goo.gl" not in url and "maps.app" not in url:
        return url
    result = subprocess.run(
        ["curl", "-sI", "-L", "--max-redirs", "5", url],
        capture_output=True, text=True, timeout=10
    )
    for line in result.stdout.splitlines():
        if line.lower().startswith("location:"):
            url = line.split(":", 1)[1].strip()
    return url


def find_data_id(maps_url: str, api_key: str) -> str:
    maps_url = resolve_url(maps_url)
    m = re.search(r"(0x[0-9a-f]+:0x[0-9a-f]+)", maps_url, re.I)
    if m:
        return m.group(1)
    m = re.search(r"/place/([^/@?#]+)", maps_url)
    place_name = urllib.parse.unquote_plus(m.group(1)).replace("+", " ") if m else maps_url
    result = serpapi_get({
        "engine": "google_maps",
        "q": place_name,
        "type": "search",
        "api_key": api_key,
        "hl": "vi",
    })
    places = result.get("local_results", [])
    if not places:
        raise SystemExit(f"ERROR: Không tìm thấy '{place_name}' trên Google Maps.")
    return places[0]["data_id"]


def fetch_all_reviews(data_id: str, api_key: str):
    all_reviews, place_info, topics = [], None, []
    token = None
    page = 0
    while True:
        params = {
            "engine": "google_maps_reviews",
            "data_id": data_id,
            "sort_by": "newestFirst",
            "num": 20,
            "api_key": api_key,
            "hl": "vi",
        }
        if token:
            params["next_page_token"] = token
        result = serpapi_get(params)
        if page == 0:
            place_info = result.get("place_info", {})
            topics = result.get("topics", [])
        reviews = result.get("reviews", [])
        all_reviews.extend(reviews)
        token = result.get("serpapi_pagination", {}).get("next_page_token")
        page += 1
        print(f"  Trang {page}: {len(reviews)} reviews (tổng: {len(all_reviews)})", file=sys.stderr)
        if not token or not reviews:
            break
    return place_info, topics, all_reviews


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 fetch-reviews.py <google_maps_url>")
    api_key = load_api_key()
    data_id = find_data_id(sys.argv[1], api_key)
    print(f"data_id: {data_id}", file=sys.stderr)
    place_info, topics, reviews = fetch_all_reviews(data_id, api_key)
    print(json.dumps(
        {"place_info": place_info, "topics": topics, "reviews": reviews, "total": len(reviews)},
        ensure_ascii=False, indent=2
    ))
