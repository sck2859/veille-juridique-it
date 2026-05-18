import feedparser
import google.generativeai as genai
import os
from datetime import datetime

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

FEEDS = {
    "RGPD & Data": [
        "https://www.cnil.fr/fr/rss.xml",
        "https://edpb.europa.eu/news/feed_en"
    ],
    "Propriété Intellectuelle": [
        "https://euipo.europa.eu/ohimportal/fr/news-rss",
        "https://www.legalis.net/feed"
    ],
    "Doctrine & Editeurs (Dalloz, Lexis, Village)": [
        "https://www.village-justice.com/articles/rss.php",
        "https://news.google.com/rss/search?q=site:dalloz-actualite.fr+OR+site:lexisnexis.fr&hl=fr&gl=FR"
    ],
    "Contrats IT & Cyber": [
        "https://www.cert.ssi.gouv.fr/feed/",
        "https://www.legalis.net/feed"
    ],
    "Droit des affaires & JP": [
        "https://www.actu-juridique.fr/feed/",
        "https://www.village-justice.com/articles/rss.php?domaine=3",
        "https://nouvelles.droit.org/feed/"
    ],
    "Réglementations européennes": [
        "https://eur-lex.europa.eu/rss/rss.xml?t=L",
        "https://www.europarl.europa.eu/rss/doc/top-stories/fr.rss",
        "https://digital-strategy.ec.europa.eu/fr/rss.xml"
    ],
    "Évolutions législatives françaises": [
        "https://www.vie-publique.fr/rss.xml",
        "https://www.senat.fr/rss/actualites.rss"
    ],
    "Jurisprudence & Doctrine": [
        "https://www.legalis.net/feed",
        "https://www.village-justice.com/articles/rss.php?domaine=2",
        "https://www.actu-juridique.fr/feed/"
    ]
}

def summarize(text):
    try:
        response = model.generate_content(f"Résume en 2 phrases simples pour un juriste IT chez Nexans : {text}")
        return response.text
    except:
        return "Pas de résumé disponible."

# --- DEBUT DU NOUVEAU DESIGN POUR LA TIMELINE ---
html_content = """<html>
<head>
    <meta charset='utf-8'>
    <title>Veille Juridique & Outils</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f7fafc; color: #2d3748; line-height: 1.6; margin: 0; padding: 40px 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { color: #1a365d; border-bottom: 3px solid #0066cc; padding-bottom: 10px; margin-bottom: 5px; }
        .update-time { color: #718096; font-size: 0.95em; margin-bottom: 40px; }
        h2 { color: #2b6cb0; margin-top: 40px; border-left: 5px solid #2b6cb0; padding-left: 10px; }
        details { background: white; padding: 15px; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border: 1px solid #e2e8f0; }
        summary { font-weight: bold; cursor: pointer; color: #2d3748; }
        summary:hover { color: #0066cc; }
        details p { margin-top: 10px; color: #4a5568; }
        a { color: #0066cc; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; }
        
        /* CSS DE LA FRISE CHRONOLOGIQUE */
        .timeline { display: flex; justify-content: space-between; align-items: flex-start; background: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; margin-bottom: 30px; overflow-x: auto; }
        .timeline-item { flex: 1; position: relative; padding: 0 15px; text-align: center; min-width: 150px; }
        .timeline-item::after { content: ''; position: absolute; top: 25px; left: 50%; width: 100%; height: 3px; background: #e2e8f0; z-index: 1; }
        .timeline-item:last-child::after { display: none; }
        .timeline-badge { width: 14px; height: 14px; background: #0066cc; border-radius: 50%; margin: 15px auto; position: relative; z-index: 2; border: 3px solid white; box-shadow: 0 0 0 2px #0066cc; }
        .timeline-date { font-weight: bold; color: #0066cc; font-size: 0.9em; text-transform: uppercase; }
        .timeline-title { font-size: 0.95em; font-weight: 700; margin-top: 5px; color: #1a202c; }
        .timeline-desc { font-size: 0.8em; color: #718096; margin-top: 5px; }
    </style>
</head>
<body>
<div class='container'>
"""

# Titre principal et date de mise à jour
html_content += f"<h1>🚀 Ma Veille Juridique Automatisée</h1>"
html_content += f"<p class='update-time'>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"

# INSERTION DE LA TIMELINE VISUELLE
html_content += """
<h2 style="border-left: 5px solid #0066cc; padding-left: 10px; color: #1a202c;">🗓️ Grandes Échéances Réglementaires IT (2026)</h2>
<div class="timeline">
    <div class="timeline-item">
        <div class="timeline-date">Courant 2026</div>
        <div class="timeline-badge"></div>
        <div class="timeline-title">Digital Omnibus</div>
        <div class="timeline-desc">Mise en conformité des modèles de contrats IT Nexans.</div>
    </div>
    <div class="timeline-item">
        <div class="timeline-date">Août 2026</div>
        <div class="timeline-badge"></div>
        <div class="timeline-title">AI Act (Paliers généraux)</div>
        <div class="timeline-desc">Premières obligations de transparence et interdictions applicables.</div>
    </div>
    <div class="timeline-item">
        <div class="timeline-date">Fin 2026</div>
        <div class="timeline-badge"></div>
        <div class="timeline-title">Révision Contrats IT</div>
        <div class="timeline-desc">Finalisation des clauses d'infogérance avec le Legal.</div>
    </div>
</div>
"""
# --- FIN DU NOUVEAU DESIGN ---

# Boucle classique de ton code pour les articles
for category, urls in FEEDS.items():
    html_content += f"<h2>📂 {category}</h2>"
    found_articles = False
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            found_articles = True
            summary = summarize(entry.title)
            html_content += f"<details style='margin-bottom:10px;'><summary><b>{entry.title}</b></summary><p>{summary}</p><a href='{entry.link}' target='_blank'>Lire l'article</a></details>"
    if not found_articles:
        html_content += "<p><i>Aucune actualité récente cette semaine.</i></p>"

# Fermeture des balises propres
html_content += "</div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
