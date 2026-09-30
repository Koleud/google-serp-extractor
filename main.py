from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from scraper import fetch_google_serp

app = FastAPI(title="Google SERP Extractor")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Google SERP Extractor</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 850px; margin: 40px auto; padding: 0 20px; line-height: 1.5; color: #202124; }
    h1 { font-size: 24px; font-weight: 600; margin-bottom: 20px; }
    .search-box { display: flex; gap: 10px; margin-bottom: 20px; }
    input[type="text"] { flex: 1; padding: 12px 16px; font-size: 16px; border: 1px solid #dfe1e5; border-radius: 24px; outline: none; box-shadow: 0 1px 6px rgba(32,33,36,.12); }
    input[type="text"]:focus { border-color: #1a73e8; }
    button { padding: 10px 20px; font-size: 15px; border-radius: 20px; border: none; cursor: pointer; font-weight: 500; transition: background 0.2s; }
    .btn-search { background: #1a73e8; color: white; }
    .btn-search:hover { background: #1557b0; }
    .btn-download { background: #188038; color: white; margin-bottom: 20px; display: none; }
    .btn-download:hover { background: #13652c; }
    .status { font-style: italic; color: #5f6368; margin-bottom: 15px; display: none; }
    .result-card { border-bottom: 1px solid #ebebeb; padding: 16px 0; }
    .result-card:last-child { border-bottom: none; }
    .result-card a { color: #1a0dab; text-decoration: none; font-size: 18px; font-weight: 500; }
    .result-card a:hover { text-decoration: underline; }
    .result-card .url { color: #202124; font-size: 13px; margin: 3px 0 6px 0; word-break: break-all; opacity: 0.8; }
    .result-card .snippet { color: #4d5156; font-size: 14px; margin: 0; }
  </style>
</head>
<body>
  
  <div class="search-box">
    <!-- Bod 1: jeden input -->
    <input type="text" id="queryInput" placeholder="Zadejte klíčové slovo..." autofocus />
    <button class="btn-search" onclick="runSearch()">Vyhledat</button>
  </div>

  <div id="status" class="status">Načítám výsledky z 1. strany Google...</div>
  <!-- Bod 3: možnost uložit na PC ve strojově čitelném formátu (JSON) -->
  <button id="downloadBtn" class="btn-download" onclick="downloadJSON()">Stáhnout výsledky (JSON)</button>
  
  <div id="results"></div>

  <script>
    let currentResults = [];

    async function runSearch() {
      const input = document.getElementById('queryInput');
      const query = input.value.trim();
      if (!query) return;

      const status = document.getElementById('status');
      const resultsDiv = document.getElementById('results');
      const downloadBtn = document.getElementById('downloadBtn');

      status.style.display = 'block';
      resultsDiv.innerHTML = '';
      downloadBtn.style.display = 'none';

      try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Chyba při komunikaci se serverem');
        
        currentResults = await response.json();

        if (currentResults.length === 0) {
          resultsDiv.innerHTML = '<p>Nebyly nalezeny žádné organické výsledky.</p>';
        } else {
          downloadBtn.style.display = 'inline-block';
          resultsDiv.innerHTML = currentResults.map(item => `
            <div class="result-card">
              <div class="url">${item.url}</div>
              <a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.title}</a>
              <p class="snippet">${item.snippet || '<i>Bez popisku</i>'}</p>
            </div>
          `).join('');
        }
      } catch (err) {
        resultsDiv.innerHTML = `<p style="color: #d93025;">Chyba: ${err.message}</p>`;
      } finally {
        status.style.display = 'none';
      }
    }

    function downloadJSON() {
      if (!currentResults.length) return;
      const dataStr = JSON.stringify(currentResults, null, 2);
      const blob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `serp_${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }

    document.getElementById('queryInput').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') runSearch();
    });
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return HTMLResponse(content=HTML_PAGE)

@app.get("/api/search")
async def search_endpoint(q: str):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Parametr 'q' nesmí být prázdný.")
    try:
        results = fetch_google_serp(q.strip())
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))