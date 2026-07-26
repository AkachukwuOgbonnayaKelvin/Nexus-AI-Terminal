"""Central Bank Registry – defines all 8 major central banks."""

from dataclasses import dataclass


@dataclass
class CentralBank:
    id: str
    name: str
    country: str
    currency: str
    timezone: str
    official_api: str | None = None
    rss_url: str | None = None
    website: str = ""
    governor: str = ""
    meeting_frequency: str = ""  # e.g., "monthly", "quarterly"
    next_meeting: str | None = None
    last_rate: float | None = None
    priority: int = 50


# Registry of all 8 major central banks
CENTRAL_BANKS = [
    CentralBank(
        id="federal_reserve",
        name="Federal Reserve",
        country="US",
        currency="USD",
        timezone="America/New_York",
        official_api="https://www.federalreserve.gov/feeds/press_all.xml",
        rss_url="https://www.federalreserve.gov/feeds/press_all.xml",
        website="https://www.federalreserve.gov/",
        governor="Jerome Powell",
        meeting_frequency="8 times per year",
        priority=100,
    ),
    CentralBank(
        id="ecb",
        name="European Central Bank",
        country="EU",
        currency="EUR",
        timezone="Europe/Frankfurt",
        official_api="https://www.ecb.europa.eu/rss/",
        rss_url="https://www.ecb.europa.eu/rss/",
        website="https://www.ecb.europa.eu/",
        governor="Christine Lagarde",
        meeting_frequency="12 times per year",
        priority=90,
    ),
    CentralBank(
        id="boe",
        name="Bank of England",
        country="UK",
        currency="GBP",
        timezone="Europe/London",
        official_api="https://www.bankofengland.co.uk/rss",
        rss_url="https://www.bankofengland.co.uk/rss",
        website="https://www.bankofengland.co.uk/",
        governor="Andrew Bailey",
        meeting_frequency="8 times per year",
        priority=85,
    ),
    CentralBank(
        id="boj",
        name="Bank of Japan",
        country="JP",
        currency="JPY",
        timezone="Asia/Tokyo",
        official_api="https://www.boj.or.jp/en/rss/",
        rss_url="https://www.boj.or.jp/en/rss/",
        website="https://www.boj.or.jp/en/",
        governor="Kazuo Ueda",
        meeting_frequency="8 times per year",
        priority=85,
    ),
    CentralBank(
        id="snb",
        name="Swiss National Bank",
        country="CH",
        currency="CHF",
        timezone="Europe/Zurich",
        official_api="https://www.snb.ch/en/rss",
        rss_url="https://www.snb.ch/en/rss",
        website="https://www.snb.ch/",
        governor="Thomas Jordan",
        meeting_frequency="4 times per year",
        priority=80,
    ),
    CentralBank(
        id="boc",
        name="Bank of Canada",
        country="CA",
        currency="CAD",
        timezone="America/Toronto",
        official_api="https://www.bankofcanada.ca/rss/",
        rss_url="https://www.bankofcanada.ca/rss/",
        website="https://www.bankofcanada.ca/",
        governor="Tiff Macklem",
        meeting_frequency="8 times per year",
        priority=80,
    ),
    CentralBank(
        id="rba",
        name="Reserve Bank of Australia",
        country="AU",
        currency="AUD",
        timezone="Australia/Sydney",
        official_api="https://www.rba.gov.au/rss/",
        rss_url="https://www.rba.gov.au/rss/",
        website="https://www.rba.gov.au/",
        governor="Michele Bullock",
        meeting_frequency="11 times per year",
        priority=75,
    ),
    CentralBank(
        id="rbnz",
        name="Reserve Bank of New Zealand",
        country="NZ",
        currency="NZD",
        timezone="Pacific/Auckland",
        official_api="https://www.rbnz.govt.nz/rss/",
        rss_url="https://www.rbnz.govt.nz/rss/",
        website="https://www.rbnz.govt.nz/",
        governor="Adrian Orr",
        meeting_frequency="7 times per year",
        priority=75,
    ),
]


def get_bank(bank_id: str) -> CentralBank | None:
    """Get a central bank by its ID."""
    for bank in CENTRAL_BANKS:
        if bank.id == bank_id:
            return bank
    return None


def get_all_banks() -> list[CentralBank]:
    """Return all banks."""
    return CENTRAL_BANKS
