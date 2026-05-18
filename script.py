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

# --- DESIGN GLOBAL AVEC TIMELINE ET CHECKLIST INTERACTIVE ---
html_content = "<html><head><meta charset='utf-8'><title>Veille Juridique & Outils</title><style>"
html_content += "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f7fafc; color: #2d3748; line-height: 1.6; margin: 0; padding: 40px 20px; }"
html_content += ".container { max-width: 1000px; margin: 0 auto; }"
html_content += "h1 { color: #1a365d; border-bottom: 3px solid #0066cc; padding-bottom: 10px; margin-bottom: 5px; }"
html_content += ".update-time { color: #718096; font-size: 0.95em; margin-bottom: 40px; }"
html_content += "h2 { color: #2b6cb0; margin-top: 40px; border-left: 5px solid #2b6cb0; padding-left: 10px; }"
html_content += "h3 { color: #4a5568; margin-top: 30px; }"
html_content += "details { background: white; padding: 15px; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border: 1px solid #e2e8f0; }"
html_content += "summary { font-weight: bold; cursor: pointer; color: #2d3748; }"
html_content += "summary:hover { color: #0066cc; }"
html_content += "details p { margin-top: 10px; color: #4a5568; }"
html_content += "a { color: #0066cc; text-decoration: none; font-weight: 500; }"
html_content += "a:hover { text-decoration: underline; }"
html_content += ".timeline { display: flex; justify-content: space-between; align-items: flex-start; background: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; margin-bottom: 30px; overflow-x: auto; }"
html_content += ".timeline-item { flex: 1; position: relative; padding: 0 15px; text-align: center; min-width: 150px; }"
html_content += ".timeline-item::after { content: ''; position: absolute; top: 25px; left: 50%; width: 100%; height: 3px; background: #e2e8f0; z-index: 1; }"
html_content += ".timeline-item:last-child::after { display: none; }"
html_content += ".timeline-badge { width: 14px; height: 14px; background: #0066cc; border-radius: 50%; margin: 15px auto; position: relative; z-index: 2; border: 3px solid white; box-shadow: 0 0 0 2px #0066cc; }"
html_content += ".timeline-date { font-weight: bold; color: #0066cc; font-size: 0.9em; text-transform: uppercase; }"
html_content += ".timeline-title { font-size: 0.95em; font-weight: 700; margin-top: 5px; color: #1a202c; }"
html_content += ".timeline-desc { font-size: 0.8em; color: #718096; margin-top: 5px; }"
html_content += ".tabs { display: flex; gap: 10px; margin-bottom: 15px; }"
html_content += ".tab-btn { padding: 10px 20px; background: #e2e8f0; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; color: #4a5568; font-size: 0.95em; }"
html_content += ".tab-btn.active { background: #0066cc; color: white; }"
html_content += ".tab-content { display: none; background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }"
html_content += ".tab-content.active { display: block; }"
html_content += ".checklist-item { margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px dashed #e2e8f0; }"
html_content += ".checklist-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }"
html_content += ".badge-alert { background: #fed7d7; color: #9b2c2c; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }"
html_content += "</style>"
html_content += "<script>function openTab(tabId) {"
html_content += "document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));"
html_content += "document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));"
html_content += "document.getElementById(tabId).classList.add('active');"
html_content += "event.currentTarget.classList.add('active');"
html_content += "}</script>"
html_content += "</head><body><div class='container'>"

# Titre principal
html_content += "<h1>🚀 Mon Tableau de Bord Juridique</h1>"
html_content += f"<p class='update-time'>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"

# TIMELINE
html_content += '<h2>🗓️ Grandes Échéances Réglementaires IT (2026)</h2>'
html_content += '<div class="timeline">'
html_content += '<div class="timeline-item"><div class="timeline-date">Courant 2026</div><div class="timeline-badge"></div><div class="timeline-title">Digital Omnibus</div><div class="timeline-desc">Mise en conformité des modèles de contrats IT Nexans.</div></div>'
html_content += '<div class="timeline-item"><div class="timeline-date">Août 2026</div><div class="timeline-badge"></div><div class="timeline-title">AI Act (Paliers généraux)</div><div class="timeline-desc">Premières obligations de transparence et interdictions applicables.</div></div>'
html_content += '<div class="timeline-item"><div class="timeline-date">Fin 2026</div><div class="timeline-badge"></div><div class="timeline-title">Révision Contrats IT</div><div class="timeline-desc">Finalisation des clauses d\'infogérance avec le Legal.</div></div>'
html_content += '</div>'

# AJOUT DE LA CHECKLIST INTERACTIVE
html_content += '<h2>🛠️ Générateur de Checklist - Clauses Obligatoires</h2>'
html_content += '<p style="color: #718096; margin-top: -10px; margin-bottom: 20px; font-size: 0.9em;">Sélectionnez le type de projet pour afficher les points de vigilance non confidentiels.</p>'
html_content += '<div class="tabs">'
html_content += '<button class="tab-btn active" onclick="openTab(\'saas\')">Cloud & SaaS</button>'
html_content += '<button class="tab-btn" onclick="openTab(\'infogerance\')">Infogérance & Maintenance</button>'
html_content += '<button class="tab-btn" onclick="openTab(\'cyber\')">Sécurité & RGPD</button>'
html_content += '</div>'

html_content += '<div id="saas" class="tab-content active">'
html_content += '<div class="checklist-item"><p><b>1. Clause de Réversibilité :</b> Vérifier les délais de restitution des données (exiger 30 jours max) et le format standard transférable (CSV, SQL).</p></div>'
html_content += '<div class="checklist-item"><p><b>2. Continuité de Service (SLA) :</b> S\'assurer que le taux de disponibilité est supérieur à 99,9% avec pénalités libératoires en cas de coupure.</p></div>'
html_content += '</div>'

html_content += '<div id="infogerance" class="tab-content">'
html_content += '<div class="checklist-item"><p><b>1. Périmètre des Lots :</b> Définition ultra-précise des prestations pour éviter les facturations "hors forfait" par le prestataire.</p></div>'
html_content += '<div class="checklist-item"><p><b>2. Transfert de personnel :</b> Attention à l\'application mécanique de l\'article L. 1224-1 du Code du travail en fin de contrat.</p></div>'
html_content += '</div>'

html_content += '<div id="cyber" class="tab-content">'
html_content += '<div class="checklist-item"><p><b>1. Localisation des Données :</b> <span class="badge-alert">Point Critique</span> Stockage impératif au sein de l\'Union Européenne (RGPD). Pas de transfert hors UE sans clauses contractuelles types.</p></div>'
html_content += '<div class="checklist-item"><p><b>2. Notification des Failles :</b> Le prestataire doit s\'engager par contrat à notifier toute violation de données sous 24h ou 48h maximum.</p></div>'
html_content += '</div>'

# BOUCLE DE LA VEILLE JURIDIQUE
html_content += "<h2>📂 Flux de Veille Automatique</h2>"
for category, urls in FEEDS.items():
    html_content += f"<h3>📂 {category}</h3>"
    found_articles = False
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            found_articles = True
            summary = summarize(entry.title)
            html_content += f"<details style='margin-bottom:10px;'><summary><b>{entry.title}</b></summary><p>{summary}</p><a href='{entry.link}' target='_blank'>Lire l'article</a></details>"
    if not found_articles:
        html_content += "<p><i>Aucune actualité récente cette semaine.</i></p>"

html_content += "</div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
