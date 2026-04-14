import feedparser
import google.generativeai as genai
import os
from datetime import datetime

# Configuration IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Sources mises à jour (Légifrance et Dalloz sont souvent capricieux)
FEEDS = {
    "RGPD & Data": ["https://www.cnil.fr/fr/rss.xml", "https://edpb.europa.eu/news/feed_en"],
    "Propriété Intellectuelle": ["https://www.inpi.fr/fr/rss.xml", "https://euipo.europa.eu/ohimportal/fr/news-rss"],
    "Contrats IT & Cyber": ["https://www.cert.ssi.gouv.fr/feed/"],
    "Évolutions Législatives": [
    "https://legifrss.org/latest",
    "https://www.vie-publique.fr/rss.xml"
],
"Jurisprudence & Doctrine": [
    "https://www.legalis.net/feed",
    "https://www.actu-juridique.fr/feed/"
]
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
