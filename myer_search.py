#!/usr/bin/env python3
"""Search Myer for products by keyword."""

from __future__ import annotations

import argparse
import json
import re
from typing import Dict, List

import requests


def search_myer(keyword: str) -> List[Dict[str, str]]:
    """Return a list of products matching the keyword."""
    url = f"https://www.myer.com.au/search?query={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    match = re.search(
        r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>',
        resp.text,
        re.DOTALL,
    )
    if not match:
        raise ValueError("Unable to locate product data")
    data = json.loads(match.group(1))

    queries = data.get("props", {}).get("pageProps", {}).get(
        "dehydratedState", {}
    ).get("queries", [])
    search_data = None
    for q in queries:
        key = q.get("queryKey")
        if isinstance(key, list) and key and key[0] == "search":
            search_data = q.get("state", {}).get("data", {})
            break
    if not search_data:
        return []

    products = search_data.get("productList", [])
    results = []
    for item in products:
        name = item.get("name", "").strip()
        price_from = item.get("priceFrom")
        price_to = item.get("priceTo")
        if price_from == price_to:
            price = f"{price_from}"
        else:
            price = f"{price_from}-{price_to}"
        details = item.get("merchCategory", "").strip()
        results.append({"name": name, "price": price, "details": details})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Myer for products")
    parser.add_argument("keyword", help="Keyword to search for")
    args = parser.parse_args()

    results = search_myer(args.keyword)
    for product in results:
        print(f"{product['name']} | {product['price']} | {product['details']}")


if __name__ == "__main__":
    main()
