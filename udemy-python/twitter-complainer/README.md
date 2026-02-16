# Internet Speed X Complainer Bot

Angela Yu–style project: measure internet speed, then post a complaint on **X** (formerly Twitter) if it’s below your promised speeds. Uses X branding and x.com URLs.

## Requirements

- Python 3.9+
- Chrome (for Selenium)
- X account (email + password)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

Set these (or put them in a `.env` file in this directory; do **not** commit `.env`):

| Variable | Required | Description |
|----------|----------|-------------|
| `X_EMAIL` | Yes | X account email (or username) |
| `X_PASSWORD` | Yes | X account password |
| `PROMISED_DOWN` | No | Promised download speed in Mbps (default: 150) |
| `PROMISED_UP` | No | Promised upload speed in Mbps (default: 10) |
| `CHROME_DRIVER_PATH` | No | Path to ChromeDriver; if unset, `webdriver-manager` downloads it |

Example `.env` (do not commit):

```
X_EMAIL=your@email.com
X_PASSWORD=your_password
PROMISED_DOWN=150
PROMISED_UP=10
```

## Run

```bash
python main.py
```

Flow: run a speed test on speedtest.net, then if down/up are below promised, log in at x.com and post a complaint.

## X UI changes

X’s web UI and DOM change often. If login or posting fails, the Selenium selectors in `main.py` may need updating. Check:

- Login: `X_USERNAME_INPUT_NAME`, `X_PASSWORD_INPUT_NAME`, and the flow (e.g. “Next” then password).
- Post composer: `data-testid="tweetTextarea_0"` and `data-testid="tweetButton"` — inspect x.com in the browser to confirm or update.

X also uses anti-bot measures; the script uses short delays between actions. If you get blocked, you may need to log in manually once or adjust behavior.
