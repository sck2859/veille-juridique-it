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
    "Contrats IT & Cyber": [
        "https://www.cert.ssi.gouv.fr/feed/"
    ],
    "Évolutions Législatives": [
        "https://www.vie-publique.fr/rss.xml",
        "https://www.senat.fr/rss/actualites.rss"
    ],
    "Jurisprudence & Doctrine": [
        "https://www.legalis.net/feed",
        "https://www.village-justice.com/articles/rss.php?domaine=2",
        "https://www.fiscalonline.com/feed"
    ]
}

def summarize(text):
    try:
        response = model.generate_content(f"Résume en 2 phrases simples pour un juriste : {text}")
        return response.text
    except:
        return "Pas de résumé disponible."

html_content = "<html><head><meta charset='utf-8'><title>Veille Juridique</title><link rel='stylesheet' href='https://cdn.simplecss.org/simple.min.css'></head><body>"
html_content += f"<h1>🚀 Ma Veille Juridique Automatisée</h1><p>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"

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

html_content += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
