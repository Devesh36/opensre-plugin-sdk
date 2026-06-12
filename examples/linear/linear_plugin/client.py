"""Linear GraphQL client."""

from __future__ import annotations

from typing import Any

import httpx

_LINEAR_API_URL = "https://api.linear.app/graphql"


class LinearClient:
    def __init__(self, *, api_key: str) -> None:
        self._api_key = api_key

    def search_issues(self, query: str) -> dict[str, Any]:
        if not self._api_key:
            return {"error": "LINEAR_API_KEY is not configured"}

        graphql_query = """
        query SearchIssues($term: String!) {
          issueSearch(query: $term, first: 10) {
            nodes {
              id
              identifier
              title
              url
              state { name }
            }
          }
        }
        """

        try:
            response = httpx.post(
                _LINEAR_API_URL,
                json={"query": graphql_query, "variables": {"term": query}},
                headers={
                    "Authorization": self._api_key,
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPError as exc:
            return {"error": f"Linear API request failed: {exc}"}

        if "errors" in payload:
            messages = "; ".join(
                str(item.get("message", item)) for item in payload.get("errors", [])
            )
            return {"error": messages or "Linear API returned errors"}

        issues = payload.get("data", {}).get("issueSearch", {}).get("nodes", [])
        return {"success": True, "issues": issues}
