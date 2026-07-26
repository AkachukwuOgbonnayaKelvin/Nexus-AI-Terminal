"""CFTC Web Crawler – discovers all reports from the CFTC website."""

import logging
import re
from datetime import datetime
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CFTCWebCrawler:
    """Crawls CFTC website to discover all available COT reports."""

    def __init__(self):
        self.base_url = "https://www.cftc.gov"
        self.historical_url = "https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalData/index.htm"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def discover_reports(self) -> list[dict[str, Any]]:
        """Discover all COT reports from the CFTC historical data page."""
        logger.info(f"Crawling CFTC historical data: {self.historical_url}")
        reports = []

        try:
            response = self.session.get(self.historical_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all links that look like COT report files
            links = soup.find_all("a", href=True)
            for link in links:
                href = link.get("href", "")
                text = link.get_text(strip=True)

                # Check if it's a COT report link
                if self._is_cot_link(href, text):
                    report = self._parse_report_link(href, text)
                    if report:
                        reports.append(report)

            logger.info(f"Found {len(reports)} reports from CFTC website")
            return reports

        except Exception as e:
            logger.error(f"Failed to crawl CFTC: {e}")
            return []

    def _is_cot_link(self, href: str, text: str) -> bool:
        """Check if a link points to a COT report."""
        href_lower = href.lower()
        text_lower = text.lower()

        # Keywords that indicate COT reports
        cot_keywords = ["cot", "commitments", "trader", "futures", "options"]
        file_extensions = [".csv", ".txt", ".zip", ".pdf"]

        # Check if it's a file link
        is_file = any(ext in href_lower for ext in file_extensions)

        # Check if it contains COT-related keywords
        is_cot = any(
            keyword in href_lower or keyword in text_lower for keyword in cot_keywords
        )

        return is_file and is_cot

    def _parse_report_link(self, href: str, text: str) -> dict[str, Any] | None:
        """Parse a report link into a structured record."""
        try:
            # Build absolute URL
            url = urljoin(self.base_url, href)

            # Extract filename
            filename = url.split("/")[-1]

            # Determine report type from filename or link text
            report_type = self._determine_report_type(filename, text)

            # Extract date if present
            date = self._extract_date(filename, text)

            return {
                "url": url,
                "filename": filename,
                "report_type": report_type,
                "date": date,
                "source": "cftc_website",
                "discovered_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.warning(f"Failed to parse link {href}: {e}")
            return None

    def _determine_report_type(self, filename: str, text: str) -> str:
        """Determine the report type from filename or text."""
        combined = f"{filename} {text}".lower()

        if "disaggregated" in combined or "disagg" in combined:
            return "disaggregated"
        elif "tff" in combined or "financial" in combined:
            return "tff"
        elif "legacy" in combined:
            return "legacy"
        elif "futures" in combined and "options" in combined:
            return "futures_options"
        elif "futures" in combined:
            return "futures"
        else:
            return "unknown"

    def _extract_date(self, filename: str, text: str) -> str | None:
        """Extract date from filename or text."""
        combined = f"{filename} {text}"

        # Look for date patterns
        patterns = [
            r"(\d{4})",  # Year
            r"(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD
            r"(\d{2}/\d{2}/\d{4})",  # MM/DD/YYYY
            r"(\d{8})",  # YYYYMMDD
        ]

        for pattern in patterns:
            match = re.search(pattern, combined)
            if match:
                return match.group(1)

        return None
