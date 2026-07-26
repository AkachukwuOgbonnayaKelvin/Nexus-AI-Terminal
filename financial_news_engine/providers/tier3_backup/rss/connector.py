from typing import Any

import feedparser

from providers.interfaces.base_provider import BaseProvider


class RSSConnector(BaseProvider):
    def __init__(self):
        self.feeds = [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.ft.com/?format=rss",
            "https://feeds.reuters.com/reuters/businessNews",
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC",
        ]
        self._connected = True
        self._tier = 3
        self._priority = 5

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> dict[str, Any] | None:
        return None

    def get_multiple(self, symbols: list[str]) -> list[dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        # Try to parse at least one feed
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                if feed.entries:
                    return True
            except Exception:
                continue
        return False

    def get_capabilities(self) -> dict[str, bool]:
        return {"news": True}

    def get_rate_limit(self) -> dict[str, int]:
        return {"requests_per_minute": 10}

    def get_available_symbols(self) -> list[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_today_news(self) -> list[dict[str, Any]]:
        results = []
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    results.append(
                        {
                            "title": entry.get("title"),
                            "summary": entry.get("summary"),
                            "link": entry.get("link"),
                            "published": entry.get("published"),
                            "author": entry.get("author"),
                            "source": feed_url.split("/")[2]
                            if "/" in feed_url
                            else "unknown",
                            "raw": entry,
                        }
                    )
            except Exception:
                continue
        return results
