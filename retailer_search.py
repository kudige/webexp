# coding: utf-8
"""Simple product searcher supporting multiple retailers."""

from __future__ import annotations

import re
from typing import Any, Dict, List

import requests


class RetailerSearcher:
    """Search for products and list categories for supported retailers.

    Parameters
    ----------
    retailer:
        Name of the retailer. Supported retailers are keys of
        :pydata:`RETAILER_ENDPOINTS`.
    """

    RETAILER_ENDPOINTS: Dict[str, Dict[str, str]] = {
        "dummyjson": {
            "categories": "https://dummyjson.com/products/categories",
            "category": "https://dummyjson.com/products/category/{category}",
            "search": "https://dummyjson.com/products/search?q={keyword}",
        },
        # Additional retailers can be added here.
    }

    def __init__(self, retailer: str) -> None:
        retailer = retailer.lower()
        if retailer not in self.RETAILER_ENDPOINTS:
            raise ValueError(f"Unsupported retailer: {retailer}")
        self.retailer = retailer
        self.endpoints = self.RETAILER_ENDPOINTS[retailer]

    def list_categories(self) -> List[str]:
        """Return available category slugs for the retailer."""
        url = self.endpoints.get("categories")
        if not url:
            raise NotImplementedError(
                f"Listing categories not supported for retailer '{self.retailer}'"
            )
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # dummyjson returns a list of objects with `slug` and `name` keys.
        if isinstance(data, list):
            # Accept either list[str] or list[dict]
            if data and isinstance(data[0], dict):
                return [c.get("slug", "") for c in data]
            return [str(c) for c in data]
        raise ValueError("Unexpected response while listing categories")

    def search(self, keyword: str, category: str | None = None) -> List[Dict[str, Any]]:
        """Search for products.

        Parameters
        ----------
        keyword:
            Keyword to search for.
        category:
            Optional category slug to limit the search.
        """
        keyword = keyword.strip()
        if not keyword:
            return []

        # Searching within a category isn't always supported natively.
        if category:
            category_url = self.endpoints.get("category")
            if not category_url:
                raise NotImplementedError(
                    f"Category search not supported for '{self.retailer}'"
                )
            url = category_url.format(category=category)
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("products", []) if isinstance(data, dict) else []
            keyword_re = re.compile(re.escape(keyword), re.I)
            return [
                item
                for item in items
                if keyword_re.search(item.get("title", ""))
                or keyword_re.search(item.get("description", ""))
            ]

        search_url = self.endpoints.get("search")
        if not search_url:
            raise NotImplementedError(
                f"General search not supported for '{self.retailer}'"
            )
        url = search_url.format(keyword=keyword)
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("products", []) if isinstance(data, dict) else []


if __name__ == "__main__":
    # Example usage when run directly
    searcher = RetailerSearcher("dummyjson")
    cats = searcher.list_categories()
    print("Categories:", ", ".join(cats[:5]), "...")
    results = searcher.search("phone", category=cats[0])
    print(f"Found {len(results)} items in category '{cats[0]}'")
