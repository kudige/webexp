# coding: utf-8
"""Simple product searcher with pluggable retailer implementations."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Type

import requests


class RetailerSearcher:
    """Base class for retailer-specific searchers."""

    retailer: str = ""

    def list_categories(self) -> List[str]:
        """Return category slugs available for the retailer."""
        raise NotImplementedError

    def search(self, keyword: str, category: str | None = None) -> List[Dict[str, Any]]:
        """Return a list of products for the given keyword and optional category."""
        raise NotImplementedError


class DummyJsonSearcher(RetailerSearcher):
    retailer = "dummyjson"
    BASE_URL = "https://dummyjson.com/products"

    def _request(self, endpoint: str, **params: str) -> Any:
        url = f"{self.BASE_URL}/{endpoint}"
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_categories(self) -> List[str]:
        data = self._request("categories")
        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                return [c.get("slug", "") for c in data]
            return [str(c) for c in data]
        raise ValueError("Unexpected response while listing categories")

    def search(self, keyword: str, category: str | None = None) -> List[Dict[str, Any]]:
        keyword = keyword.strip()
        if not keyword:
            return []
        if category:
            data = self._request(f"category/{category}")
            items = data.get("products", []) if isinstance(data, dict) else []
            keyword_re = re.compile(re.escape(keyword), re.I)
            return [
                item
                for item in items
                if keyword_re.search(item.get("title", ""))
                or keyword_re.search(item.get("description", ""))
            ]
        data = self._request("search", q=keyword)
        return data.get("products", []) if isinstance(data, dict) else []


RETAILER_MAP: Dict[str, Type[RetailerSearcher]] = {
    DummyJsonSearcher.retailer: DummyJsonSearcher,
}


def create_searcher(retailer: str) -> RetailerSearcher:
    """Return a searcher instance for the given retailer."""
    retailer = retailer.lower()
    if retailer not in RETAILER_MAP:
        raise ValueError(f"Unsupported retailer: {retailer}")
    return RETAILER_MAP[retailer]()


if __name__ == "__main__":
    # Example usage when run directly
    searcher = create_searcher("dummyjson")
    cats = searcher.list_categories()
    print("Categories:", ", ".join(cats[:5]), "...")
    results = searcher.search("phone", category=cats[0])
    print(f"Found {len(results)} items in category '{cats[0]}'")
