# Hive RNS News Log

Railway worker that scrapes Investegate **today’s announcements**, matches them to
tickers from **UK AIM Micro-Cap**, and **automatically writes** each hit into
Notion **Hive RNS News Log** with AI Summary when available.

Does **not** modify the hive-bot Telegram app or the existing R_News repo.

## What gets written (Hive RNS News Log)

| Property   | Source |
|-----------|--------|
| Title     | RNS headline |
| Ticker    | Matched from Micro-Cap universe |
| Company   | Investegate company cell |
| Link      | Full RNS URL |
| AI Summary| Scraped from Investegate AI summary block |
| RNS Date  | Scan date (UTC) |
| RNS Hash  | Dedup key (MD5) |
| Source    | `Investegate` |

Also updates the matched **UK AIM Micro-Cap** page:
- Last RNS Date
- Last 3 RNS (rolling)

## Railway setup

1. New Railway project → Deploy from this GitHub repo
2. Add volume mounted at `/data` (persists `last_rns_ids.txt`)
3. Set variables from `.env.example`
4. Share both Notion databases with the integration:
   - Hive RNS News Log
   - UK AIM Micro-Cap
   - (optional) Hive Bot Watchlist

## Local one-shot

```bash
export NOTION_TOKEN=...
export NOTION_TICKERS_DB_ID=...
export NOTION_RNS_DB_ID=a7931699-9ab9-4fe6-8a81-74d86146ae1a
python bot.py
```

## Loop worker

```bash
python worker.py
```
