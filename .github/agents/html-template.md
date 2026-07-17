# HTML Dashboard Template — Media Plan CI

Dieses Template ist die verbindliche Vorlage für alle HTML-Dashboards im Media Plan CI.
Der Agent ersetzt ausschließlich die mit `{{PLATZHALTER}}` markierten Stellen.
CSS, Struktur und Klassenbezeichnungen bleiben unverändert.

---

## Verwendung durch den Agenten

1. Dieses Template 1:1 als Basis verwenden
2. Nur `{{PLATZHALTER}}` ersetzen — niemals CSS-Variablen oder Klassen umbenennen
3. Logo-Base64 aus dem Agenten-Wissen einsetzen (Datei: `logo_b64.txt`)
4. Nicht benötigte Blöcke vollständig entfernen (z.B. Controls wenn kein Filter nötig)
5. Datendichte JSON-Objekt in `<script>` einbetten — alle Berechnungen vorher in Python

---

## Verfügbare CI-Farben

| Variable        | Hex       | Verwendung                          |
|-----------------|-----------|-------------------------------------|
| `--navy`        | `#13355A` | Header, aktive Buttons, Überschriften |
| `--teal`        | `#1D666F` | Akzent, Kernaussage-Border, KPI grün |
| `--teal-dk`     | `#042B30` | Tooltip-Hintergrund, Text dunkel    |
| `--grey`        | `#D6D6D6` | Borders, Trennlinien                |
| `--beige`       | `#B3A69E` | Sekundäre Kurvenfarbe               |
| `--lblue`       | `#A2C1C4` | Tertiäre Kurvenfarbe                |
| `--bg`          | `#EEF1F5` | Seitenhintergrund                   |
| `--surface`     | `#FFFFFF` | Kartenhintergrund                   |
| `--border`      | `#D6D6D6` | Rahmen aller Karten                 |
| `--text`        | `#042B30` | Primärtext                          |
| `--muted`       | `#6B7A8D` | Sekundärtext, Labels                |

### Kurvenfarben (Reihenfolge einhalten)
```
['#13355A', '#1D666F', '#A2C1C4', '#B3A69E', '#042B30', '#7A9EAA', '#6B7A8D']
```

### KPI-Ampelfarben
- **Grün / gut:** `color: var(--teal)` → Klasse `kpi-green` / `pct-hi`
- **Gelb / mittel:** `color: #B3821A` → Klasse `kpi-yellow` / `pct-mid`
- **Rot / schlecht:** `color: #C0392B` → Klasse `kpi-red` / `pct-lo`

---

## Vollständiges HTML-Template

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{SEITENTITEL}}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --navy:    #13355A;
    --teal:    #1D666F;
    --teal-dk: #042B30;
    --grey:    #D6D6D6;
    --beige:   #B3A69E;
    --lblue:   #A2C1C4;
    --bg:      #EEF1F5;
    --surface: #FFFFFF;
    --border:  #D6D6D6;
    --text:    #042B30;
    --muted:   #6B7A8D;
  }
  body { background:var(--bg); font-family:'Inter',sans-serif; color:var(--text); min-height:100vh; }

  /* ── HEADER ── */
  header {
    background:var(--navy); padding:0 36px;
    display:flex; align-items:center; gap:20px; height:64px;
    box-shadow:0 2px 8px rgba(4,43,48,.2);
  }
  .logo-img { height:30px; width:auto; filter:brightness(0) invert(1); flex-shrink:0; }
  .hdr-div { width:1px; height:28px; background:rgba(255,255,255,.2); }
  header h1 { font-size:15px; font-weight:600; color:#fff; letter-spacing:.01em; }

  /* ── CONTROLS (optional – entfernen wenn kein Filter benötigt) ── */
  .controls {
    background:var(--surface); padding:14px 36px;
    display:flex; gap:28px; flex-wrap:wrap; align-items:center;
    border-bottom:1px solid var(--border); box-shadow:0 1px 3px rgba(0,0,0,.06);
  }
  .ctrl-group { display:flex; align-items:center; gap:10px; }
  .ctrl-label { font-size:11px; font-weight:700; color:var(--muted); letter-spacing:.07em; text-transform:uppercase; white-space:nowrap; }
  .btn-group { display:flex; border-radius:6px; overflow:hidden; border:1px solid var(--border); }
  .btn-group button {
    background:#fff; border:none; padding:7px 16px;
    font-size:12.5px; font-weight:500; color:var(--muted);
    cursor:pointer; font-family:'Inter',sans-serif;
    border-right:1px solid var(--border); transition:background .15s,color .15s;
  }
  .btn-group button:last-child { border-right:none; }
  .btn-group button:hover { background:var(--bg); color:var(--navy); }
  .btn-group button.active { background:var(--navy); color:#fff; font-weight:600; }

  /* ── MAIN ── */
  main { padding:24px 36px; }

  /* ── KERNAUSSAGE (optional) ── */
  .reco-box {
    background:var(--surface); border:1px solid var(--border);
    border-left:4px solid var(--teal); border-radius:8px;
    padding:16px 20px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,.05);
  }
  .reco-box h3 { font-size:10.5px; font-weight:700; color:var(--teal); letter-spacing:.07em; text-transform:uppercase; margin-bottom:7px; }
  .reco-box p { font-size:13px; color:var(--muted); line-height:1.7; }
  .reco-box p strong { color:var(--text); }

  /* ── SECTION LABEL ── */
  .section-title { font-size:10px; font-weight:700; letter-spacing:.09em; text-transform:uppercase; color:var(--muted); margin-bottom:12px; margin-top:20px; }

  /* ── KPI KACHELN (optional) ── */
  /* Anzahl Spalten anpassen: repeat(4,1fr) für 4 Kacheln usw. */
  .kpi-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:20px; }
  .kpi-card { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:14px 16px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,.05); }
  .kpi-label { font-size:10px; color:var(--muted); font-weight:700; letter-spacing:.07em; text-transform:uppercase; margin-bottom:6px; }
  .kpi-val { font-size:26px; font-weight:700; }
  .kpi-sub { font-size:10px; color:var(--muted); margin-top:3px; }
  .kpi-green { color:var(--teal); }
  .kpi-yellow { color:#B3821A; }
  .kpi-red { color:#C0392B; }

  /* ── CHART + TABELLE NEBENEINANDER ── */
  /* Verhältnis anpassen: 1fr 1fr für gleich breit, 2fr 1fr für breites Chart */
  .chart-table-grid { display:grid; grid-template-columns:1.4fr 1fr; gap:16px; }
  @media(max-width:860px){ .chart-table-grid { grid-template-columns:1fr; } }

  /* ── KARTE (für Chart oder Tabelle) ── */
  .chart-card { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,.05); }
  .chart-card h3 { font-size:13px; font-weight:600; color:var(--navy); margin-bottom:2px; }
  .chart-card .note { font-size:11px; color:var(--muted); margin-bottom:14px; }

  /* ── LEGENDE (für Charts) ── */
  .legend { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:12px; }
  .leg-item { display:flex; align-items:center; gap:5px; font-size:11px; color:var(--muted); }
  .leg-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }

  /* ── TABELLE ── */
  .data-table { width:100%; border-collapse:collapse; font-size:12px; }
  .data-table th { background:var(--bg); color:var(--muted); font-weight:700; padding:8px 10px; text-align:right; border-bottom:2px solid var(--border); font-size:10.5px; letter-spacing:.05em; text-transform:uppercase; }
  .data-table th:first-child { text-align:left; }
  .data-table td { padding:7px 10px; text-align:right; border-bottom:1px solid #EAECEF; font-variant-numeric:tabular-nums; }
  .data-table td:first-child { text-align:left; font-weight:500; color:var(--navy); }
  .data-table tr:last-child td { border-bottom:none; }
  .data-table tr:hover td { background:var(--bg); }
  /* Wertklassen für farbige Tabellenzellen */
  .pct-cell { font-weight:600; }
  .pct-hi { color:var(--teal); }
  .pct-mid { color:#B3821A; }
  .pct-lo { color:#C0392B; }
  /* Summen-/Schnittzeile */
  .sum-row td { border-top:2px solid var(--border) !important; color:var(--muted); font-size:11px; background:var(--bg); }

  /* ── FOOTER / ERKLÄRTEXT (optional) ── */
  footer { margin:24px 36px 36px; padding:18px 22px; background:var(--surface); border:1px solid var(--border); border-radius:8px; box-shadow:0 1px 4px rgba(0,0,0,.05); }
  .footer-title { font-size:10px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-bottom:10px; }
  footer p { font-size:12.5px; color:var(--muted); line-height:1.75; }
  footer p + p { margin-top:7px; }
  footer strong { color:var(--text); }

  @media(max-width:860px){ main,header,.controls,footer { padding-left:16px; padding-right:16px; } }
</style>
</head>
<body>

<!-- ══════════════════════════════════════════════
     BLOCK 1: HEADER — immer vorhanden
     Logo-Base64 aus logo_b64.txt einsetzen
     ══════════════════════════════════════════════ -->
<header>
  <img class="logo-img" src="data:image/png;base64,{{LOGO_BASE64}}" alt="Media Plan Logo">
  <div class="hdr-div"></div>
  <h1>{{DASHBOARD_TITEL}}</h1>
</header>

<!-- ══════════════════════════════════════════════
     BLOCK 2: CONTROLS — nur wenn Filter/Auswahl vorhanden
     Nicht benötigte ctrl-groups einfach entfernen
     ══════════════════════════════════════════════ -->
<div class="controls">
  <div class="ctrl-group">
    <span class="ctrl-label">{{FILTER_LABEL_1}}</span>
    <div class="btn-group" id="bg-filter1">
      <button class="active" onclick="setFilter('filter1','{{OPTION_A}}',this)">{{OPTION_A_LABEL}}</button>
      <button onclick="setFilter('filter1','{{OPTION_B}}',this)">{{OPTION_B_LABEL}}</button>
      <!-- weitere Optionen nach Bedarf -->
    </div>
  </div>
  <!-- weitere ctrl-groups nach Bedarf -->
</div>

<!-- ══════════════════════════════════════════════
     BLOCK 3: HAUPTINHALT
     ══════════════════════════════════════════════ -->
<main>

  <!-- KERNAUSSAGE — optional, entfernen wenn nicht benötigt -->
  <div class="reco-box">
    <h3>Kernaussage</h3>
    <p id="reco-text">{{KERNAUSSAGE_TEXT_ODER_DYNAMISCH_PER_JS}}</p>
  </div>

  <!-- KPI KACHELN — optional -->
  <!-- section-title beschreibt den Kontext der Kacheln -->
  <div class="section-title">{{KPI_ABSCHNITT_TITEL}}</div>
  <div class="kpi-grid">
    <!-- Statisches Beispiel: -->
    <div class="kpi-card">
      <div class="kpi-label">{{KPI_LABEL_1}}</div>
      <div class="kpi-val kpi-green">{{KPI_WERT_1}}</div>
      <div class="kpi-sub">{{KPI_UNTERTITEL_1}}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">{{KPI_LABEL_2}}</div>
      <div class="kpi-val kpi-yellow">{{KPI_WERT_2}}</div>
      <div class="kpi-sub">{{KPI_UNTERTITEL_2}}</div>
    </div>
    <!-- weitere Kacheln nach Bedarf — bei dynamischen Werten per JS befüllen -->
    <div id="kpi-grid-dynamic"></div>
  </div>

  <!-- CHART + TABELLE — Hauptvisualisierung -->
  <div class="chart-table-grid">

    <!-- Linien-/Balkendiagramm -->
    <div class="chart-card">
      <h3 id="chart-title">{{CHART_TITEL}}</h3>
      <p class="note">{{CHART_UNTERTITEL}}</p>
      <!-- Legende — bei dynamischen Serien per JS befüllen -->
      <div class="legend" id="chart-legend">
        <div class="leg-item"><span class="leg-dot" style="background:#13355A"></span>{{SERIE_1}}</div>
        <div class="leg-item"><span class="leg-dot" style="background:#1D666F"></span>{{SERIE_2}}</div>
      </div>
      <canvas id="main-chart"></canvas>
    </div>

    <!-- Tabelle -->
    <div class="chart-card">
      <h3>{{TABELLEN_TITEL}}</h3>
      <p class="note">{{TABELLEN_UNTERTITEL}}</p>
      <table class="data-table">
        <thead>
          <tr>
            <th>{{SPALTE_1}}</th>
            <th>{{SPALTE_2}}</th>
            <th>{{SPALTE_3}}</th>
            <!-- weitere Spalten nach Bedarf -->
          </tr>
        </thead>
        <tbody id="table-body">
          <!-- Zeilen per JS befüllen oder statisch einsetzen -->
        </tbody>
      </table>
    </div>

  </div><!-- end chart-table-grid -->

</main>

<!-- ══════════════════════════════════════════════
     BLOCK 4: ERKLÄRTEXT — optional
     Entfernen wenn keine Methodikerklärung nötig
     ══════════════════════════════════════════════ -->
<footer>
  <p class="footer-title">{{ERKLAERTEXT_TITEL}}</p>
  <p>{{ERKLAERTEXT_ABSATZ_1}}</p>
  <p>{{ERKLAERTEXT_ABSATZ_2}}</p>
</footer>

<!-- ══════════════════════════════════════════════
     JAVASCRIPT
     Alle Daten als JSON einbetten, kein externer Datenabruf
     ══════════════════════════════════════════════ -->
<script>
// ── DATEN (aus Python/pandas berechnet und hier eingebettet) ──
const DATA = {{JSON_DATEN}};

// ── KONFIGURATION ──
const COLORS = ['#13355A','#1D666F','#A2C1C4','#B3A69E','#042B30','#7A9EAA','#6B7A8D'];

// ── FILTER-STATE (falls Controls vorhanden) ──
let state = { filter1: '{{OPTION_A}}' };
let chartInstance = null;

// ── FILTER UMSCHALTEN ──
function setFilter(type, val, btn) {
  state[type] = val;
  const groupId = { filter1: 'bg-filter1' }[type];
  document.getElementById(groupId).querySelectorAll('button')
    .forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  render();
}

// ── HAUPTRENDER-FUNKTION ──
function render() {
  // 1. Daten für aktuellen State selektieren
  const currentData = DATA[state.filter1]; // Beispiel — an Datenstruktur anpassen

  // 2. KPI-Kacheln befüllen (Beispiel für dynamische Befüllung)
  // document.getElementById('kpi-grid-dynamic').innerHTML = ...

  // 3. Kernaussage befüllen (optional, falls dynamisch)
  // document.getElementById('reco-text').innerHTML = ...

  // 4. Chart rendern
  const ctx = document.getElementById('main-chart');
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(ctx, {
    type: 'line', // 'bar', 'line', 'pie', 'doughnut' etc.
    data: {
      labels: {{X_ACHSE_LABELS}}, // z.B. ['Jan','Feb','Mär',...]
      datasets: [
        {
          label: '{{SERIE_1}}',
          data: {{SERIE_1_DATEN}},
          borderColor: COLORS[0],
          backgroundColor: 'transparent',
          borderWidth: 2,
          pointRadius: 4,
          tension: 0.3,
        },
        // weitere Serien nach Bedarf
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false }, // eigene Legende oben
        tooltip: {
          backgroundColor: '#042B30',
          borderColor: '#1D666F',
          borderWidth: 1,
          titleColor: '#fff',
          bodyColor: '#A2C1C4',
          padding: 10,
        }
      },
      scales: {
        x: {
          grid: { color: '#EAECEF' },
          ticks: { color: '#6B7A8D', font: { size: 11 } },
        },
        y: {
          grid: { color: '#EAECEF' },
          ticks: { color: '#6B7A8D', font: { size: 11 } },
        }
      }
    }
  });

  // 5. Tabelle befüllen
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = currentData.map(row => `
    <tr>
      <td>${row.label}</td>
      <td class="pct-cell pct-hi">${row.value1}</td>
      <td>${row.value2}</td>
    </tr>
  `).join('');
}

// ── INITIALER AUFRUF ──
render();
</script>
</body>
</html>
```

---

## Verfügbare Block-Kombinationen

Je nach Aufgabenstellung nur die benötigten Blöcke verwenden:

| Szenario | Blöcke |
|---|---|
| Einfache KPI-Übersicht | Header + KPI-Kacheln |
| Zeitreihen-Analyse | Header + Chart (Linie) |
| Vergleich mehrerer Dimensionen | Header + Controls + Chart |
| Vollständiges Reporting-Dashboard | Header + Controls + Kernaussage + KPIs + Chart + Tabelle + Footer |
| Nur Tabelle mit Erklärung | Header + Tabelle + Footer |

## Chart.js Typen (Auswahl)

| Typ | `type`-Wert | Wann verwenden |
|---|---|---|
| Linienchart | `'line'` | Zeitreihen, Verläufe |
| Balkendiagramm | `'bar'` | Kategorienvergleich |
| Horizontale Balken | `'bar'` + `indexAxis:'y'` | Rangfolgen |
| Kreisdiagramm | `'doughnut'` | Anteile (max. 5 Segmente) |
| Gestapelte Balken | `'bar'` + `stacked:true` | Zusammensetzung |

## Hinweise für den Agenten

- **Niemals** externe Dateien oder API-Calls im fertigen HTML — alles inline
- **Niemals** CSS-Variablennamen oder Klassennamen ändern
- Logo-Base64 ist im Agenten-Wissen hinterlegt — direkt einsetzen, nicht neu laden
- Bei Unsicherheit über Diagrammtyp: Linie für Zeitreihen, Balken für Kategorien
- `{{PLATZHALTER}}` die nicht benötigt werden vollständig entfernen (kein leerer Text)
- Fertige Datei immer nach `/mnt/data/{{DATEINAME}}.html` speichern
