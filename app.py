"""
Flask app for route optimizer: serve frontend and /optimize API.
"""

import logging
import os

from flask import Flask, jsonify, render_template_string, request

from route_logic import DEFAULT_COORDS, optimize_route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json(force=True, silent=True) or {}
    origin = (data.get("origin") or "").strip() or "Sebring, FL"
    stops = data.get("stops") or []
    if isinstance(stops, str):
        stops = [s.strip() for s in stops.split("\n") if s.strip()]
    result = optimize_route(origin, stops, coords_cache=DEFAULT_COORDS)
    return jsonify(result)


# Embedded HTML template (single-file app for easy sharing)
INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Route Optimizer</title>
  <style>
    :root {
      --bg: #0f1419;
      --surface: #1a2332;
      --border: #2d3a4f;
      --text: #e6edf3;
      --muted: #8b9cb8;
      --accent: #58a6ff;
      --accent-hover: #79b8ff;
      --success: #3fb950;
      --error: #f85149;
    }
    * { box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 1.5rem;
      line-height: 1.5;
      min-height: 100vh;
    }
    .container { max-width: 560px; margin: 0 auto; }
    h1 { font-size: 1.5rem; font-weight: 600; margin: 0 0 1rem; color: var(--text); }
    label { display: block; font-size: 0.875rem; color: var(--muted); margin-bottom: 0.25rem; }
    input, textarea, button {
      width: 100%;
      padding: 0.6rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      color: var(--text);
      font-size: 1rem;
    }
    input::placeholder, textarea::placeholder { color: var(--muted); }
    textarea { min-height: 120px; resize: vertical; }
    .field { margin-bottom: 1rem; }
    button {
      cursor: pointer;
      font-weight: 600;
      background: var(--accent);
      color: var(--bg);
      border: none;
      margin-top: 0.5rem;
    }
    button:hover { background: var(--accent-hover); }
    button.secondary {
      background: var(--surface);
      color: var(--accent);
      border: 1px solid var(--border);
      width: auto;
      padding: 0.4rem 0.75rem;
      font-size: 0.875rem;
    }
    button.secondary:hover { border-color: var(--accent); }
    #result { margin-top: 1.5rem; padding: 1rem; border-radius: 8px; background: var(--surface); border: 1px solid var(--border); display: none; }
    #result.show { display: block; }
    #result.error { border-color: var(--error); }
    #result .total { font-size: 1.125rem; font-weight: 600; color: var(--success); margin-bottom: 0.5rem; }
    #result ol { margin: 0.5rem 0; padding-left: 1.25rem; }
    #result li { margin: 0.25rem 0; }
    #result .map-link { margin-top: 0.75rem; }
    #result .map-link a { color: var(--accent); word-break: break-all; }
    #result .map-link a:hover { text-decoration: underline; }
    .copy-wrap { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap; }
    .copy-wrap input { flex: 1; min-width: 0; }
    .spinner { display: none; }
    .spinner.show { display: inline-block; animation: spin 0.8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="container">
    <h1>Route Optimizer</h1>
    <p style="color: var(--muted); font-size: 0.875rem; margin-bottom: 1rem;">
      Enter start/end and all stops. We’ll find the fastest driving order and give you a Google Maps link.
    </p>
    <form id="form">
      <div class="field">
        <label for="origin">Start &amp; end</label>
        <input type="text" id="origin" name="origin" value="Sebring, FL" placeholder="e.g. Sebring, FL">
      </div>
      <div class="field">
        <label for="stops">Stops (one per line)</label>
        <textarea id="stops" name="stops" placeholder="2308 Oakdale St S, St. Petersburg, FL 33705&#10;4718 Belfast Dr, New Port Richey, FL 34652&#10;...">2308 Oakdale St S, St. Petersburg, FL 33705
4718 Belfast Dr, New Port Richey, FL 34652
3006 E Dr MLK Jr Blvd, Tampa, FL 33610
1502 Valrico Lake Rd, Valrico, FL 33594
2420 Chestnut Woods Dr, Lakeland, FL 33815</textarea>
      </div>
      <button type="submit" id="btn">
        <span id="btnText">Optimize route</span>
        <span class="spinner" id="spinner">⟳</span>
      </button>
    </form>
    <div id="result">
      <div class="total" id="total"></div>
      <ol id="order"></ol>
      <div class="map-link">
        <strong>Map:</strong>
        <a id="mapLink" href="#" target="_blank" rel="noopener"></a>
        <div class="copy-wrap">
          <input type="text" id="mapUrlCopy" readonly>
          <button type="button" class="secondary" id="copyBtn">Copy link</button>
        </div>
      </div>
    </div>
  </div>
  <script>
    const form = document.getElementById('form');
    const result = document.getElementById('result');
    const totalEl = document.getElementById('total');
    const orderEl = document.getElementById('order');
    const mapLink = document.getElementById('mapLink');
    const mapUrlCopy = document.getElementById('mapUrlCopy');
    const copyBtn = document.getElementById('copyBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('spinner');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      result.classList.remove('show', 'error');
      btnText.style.display = 'none';
      spinner.classList.add('show');
      const origin = document.getElementById('origin').value.trim();
      const stopsText = document.getElementById('stops').value.trim();
      const stops = stopsText ? stopsText.split('\n').map(s => s.trim()).filter(Boolean) : [];
      try {
        const res = await fetch('/optimize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ origin, stops })
        });
        const data = await res.json();
        if (data.ok) {
          totalEl.textContent = 'Total drive time: ' + data.total_duration;
          orderEl.innerHTML = data.legs.map(l => '<li>' + escapeHtml(l.address) + ' <small>(' + l.leg_minutes + ' min)</small></li>').join('');
          mapLink.href = data.map_url;
          mapLink.textContent = 'Open in Google Maps';
          mapUrlCopy.value = data.map_url;
          result.classList.add('show');
        } else {
          totalEl.textContent = 'Error: ' + (data.error || 'Unknown error');
          orderEl.innerHTML = '';
          mapLink.href = '#';
          mapUrlCopy.value = '';
          result.classList.add('show', 'error');
        }
      } catch (err) {
        totalEl.textContent = 'Error: ' + (err.message || 'Request failed');
        result.classList.add('show', 'error');
      } finally {
        btnText.style.display = '';
        spinner.classList.remove('show');
      }
    });

    copyBtn.addEventListener('click', () => {
      mapUrlCopy.select();
      document.execCommand('copy');
      copyBtn.textContent = 'Copied!';
      setTimeout(() => { copyBtn.textContent = 'Copy link'; }, 2000);
    });

    function escapeHtml(s) {
      const div = document.createElement('div');
      div.textContent = s;
      return div.innerHTML;
    }
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
