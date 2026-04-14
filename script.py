import feedparser
import google.generativeai as genai
import os
from datetime import datetime

# Configuration IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Sources Juridiques M1 (JP, Lois, Data)
FEEDS = {
    "⚖️ Jurisprudence & Doctrine": [
        "https://www.courdecassation.fr/rss/all",
        "https://www.dalloz-actualite.fr/rss.xml"
    ],
    "🏛️ Projets de Loi & Parlement": [
        "https://www.senat.fr/rss/projets_de_loi.xml",
        "https://www.assemblee-nationale.fr/rss/projets-de-loi.xml"
    ],
    "💻 Droit du Numérique & IA": [
        "https://www.cnil.fr/fr/rss.xml",
        "https://edpb.europa.eu/news/feed_en"
    ]
}

def summarize(text):
    try:
        response = model.generate_content(f"Résume en 2 phrases pour une juriste de M1 : {text}")
        return response.text
    except:
        return "Résumé non disponible."

html_content = """
<html>
<head>
    <meta charset='utf-8'>
    <title>Veille Juridique IT - Nexans</title>
    <link rel='stylesheet' href='https://cdn.simplecss.org/simple.min.css'>
    <style>
        body { max-width: 900px; }
        details { background: #f4f4f4; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
        summary { font-weight: bold; cursor: pointer; color: #d32f2f; }
    </style>
</head>
<body>
    <header>
        <h1>🚀 Ma Veille Juridique IT</h1>
        <p>Mise à jour le : <b>""" + datetime.now().strftime('%d/%m/%Y à %H:%M') + """</b></p>
    </header>
    <section>
        <p><i>Bienvenue dans ton espace de veille. Ce site analyse les flux de la Cour de Cassation, du Parlement et de la CNIL.</i></p>
    </section>
"""

for category, urls in FEEDS.items():
    html_content += f"<h2>{category}</h2>"
    count = 0
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            count += 1
            summary = summarize(entry.title)
            html_content += f"""
            <details>
                <summary>{entry.title}</summary>
                <p>{summary}</p>
                <a href='{entry.link}' target='_blank'>Consulter la source officielle</a>
            </details>
            """
    if count == 0:
        html_content += "<p><i>Rien de neuf dans cette catégorie aujourd'hui.</i></p>"

html_content += "<footer><p>M1 Droit du Numérique - Nexans 2026</p></footer></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
