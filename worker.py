#!/usr/bin/env python3
"""
Hive RNS News Log worker – scan Investegate, match tickers, write Notion.

On every new RNS match, bot.check_rns():
  1) Telegram channel + optional watchlist DMs
  2) Creates a row in Notion «Hive RNS News Log» (Ticker, Company, Title,
     Link, AI Summary, RNS Date, RNS Hash, Source)
  3) Updates Last RNS Date + Last 3 RNS on UK AIM Micro-Cap security page
"""

from __future__ import annotations

import os
import sys
import time
import traceback
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None  # type: ignore

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

STATE_DIR = os.getenv("STATE_DIR", ".").strip() or "."
os.makedirs(STATE_DIR, exist_ok=True)
os.environ.setdefault(
    "RNS_STATE_FILE",
    os.path.join(STATE_DIR, "last_rns_ids.txt"),
)

INTERVAL_OFF = max(1, int(os.getenv("SCAN_INTERVAL_MINUTES", "5")))
INTERVAL_MKT = max(1, int(os.getenv("SCAN_INTERVAL_MARKET_MIN", "2")))


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _london_now():
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("Europe/London"))
    return datetime.now(timezone.utc)


def _is_uk_market_hours() -> bool:
    now = _london_now()
    if now.weekday() >= 5:
        return False
    minutes = now.hour * 60 + now.minute
    return (7 * 60) <= minutes <= (16 * 60 + 30)


def _next_interval_min() -> int:
    return INTERVAL_MKT if _is_uk_market_hours() else INTERVAL_OFF


def _env_check() -> None:
    for key in ("NOTION_TOKEN", "NOTION_TICKERS_DB_ID", "NOTION_RNS_DB_ID"):
        if not os.getenv(key):
            print(f"[{_ts()}] WARNING: {key} not set – Notion auto-sync incomplete")
    if not os.getenv("TELEGRAM_TOKEN"):
        print(f"[{_ts()}] WARNING: TELEGRAM_TOKEN not set – Telegram alerts disabled")


def run_once() -> None:
    print(f"[{_ts()}] RNS scan cycle start")
    try:
        from bot import check_rns

        check_rns()
    except Exception as e:
        print(f"[{_ts()}] bot.check_rns error: {e}")
        traceback.print_exc()
    wait = _next_interval_min()
    print(f"[{_ts()}] Cycle done – next scan in {wait} minute(s)")


def main() -> None:
    _env_check()
    print(
        f"[{_ts()}] Hive-RNS-News-Log worker starting "
        f"(market={INTERVAL_MKT}m, off={INTERVAL_OFF}m, state_dir={STATE_DIR})"
    )
    while True:
        run_once()
        time.sleep(_next_interval_min() * 60)


if __name__ == "__main__":
    main()
