#!/usr/bin/env python3
"""Search Myer for products by keyword."""

from __future__ import annotations

import argparse
import json
import re
from typing import Dict, List

import requests


def search_myer(keyword: str, department: str | None = None) -> List[Dict[str, str]]:
    """Return a list of products matching the keyword.

    Parameters
    ----------
    keyword:
        Term to search for.
    department:
        Optional department slug to scope the search, e.g. ``"beauty"``.
    """
    url = f"https://www.myer.com.au/search?query={keyword}"
    if department:
        url += f"&department={department}"
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
        seo_token = item.get("seoToken", "")
        product_url = f"https://www.myer.com.au/p/{seo_token}" if seo_token else ""
        results.append({
            "name": name,
            "price": price,
            "details": details,
            "url": product_url,
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Myer for products")
    parser.add_argument("keyword", help="Keyword to search for")
    parser.add_argument(
        "--department",
        help="Department slug to filter results (e.g. 'beauty')",
    )
    parser.add_argument(
        "--show-url",
        action="store_true",
        help="Display the product URL for each result",
    )
    args = parser.parse_args()

    results = search_myer(args.keyword, department=args.department)
    for product in results:
        line = f"{product['name']} | {product['price']} | {product['details']}"
        if args.show_url and product.get("url"):
            line += f" | {product['url']}"
        print(line)


if __name__ == "__main__":
    main()
