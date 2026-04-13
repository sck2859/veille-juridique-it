import feedparser
import google.generativeai as genai
import os
from datetime import datetime

# Configuration de l'IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Sources de veille
FEEDS = {
    "RGPD & Data": ["https://www.cnil.fr/fr/rss.xml", "https://edpb.europa.eu/news/feed_en"],
    "Propriété Intellectuelle": ["https://www.inpi.fr/fr/rss.xml", "https://euipo.europa.eu/ohimportal/fr/news-rss"],
    "Contrats IT & Cyber": ["https://www.cert.ssi.gouv.fr/feed/"],
    "Évolutions Législatives": ["https://www.legifrance.gouv.fr/jorf/rss"],
    "Doctrine & Jurisprudence": ["https://www.dalloz-actualite.fr/rss.xml"]
}

def summarize(text):
    try:
        prompt = f"Tu es une juriste experte. Résume cet article en 3 lignes max pour un dashboard pro : {text}"
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Résumé indisponible."

# Création du fichier HTML
html_content = "<html><head><meta charset='utf-8'><title>Ma Veille Juridique</title><link rel='stylesheet' href='https://cdn.simplecss.org/simple.min.css'></head><body>"
html_content += f"<h1>🚀 Ma Veille Juridique Automatisée</h1><p>Mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"

for category, urls in FEEDS.items():
    html_content += f"<h2>📂 {category}</h2>"
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            summary = summarize(entry.title + " " + entry.get('summary', ''))
            html_content += f"<details><summary><b>{entry.title}</b></summary><p>{summary}</p><a href='{entry.link}' target='_blank'>Lire l'article</a></details>"

html_content += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
