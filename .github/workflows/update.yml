"""
Veille Juridique IT — script d'automatisation.

Architecture :
1. On va chercher les derniers articles sur des flux RSS juridiques, classés par catégorie.
2. Pour chaque nouvel article (pas déjà connu), on demande à Gemini de rédiger
   une fiche d'analyse structurée (JSON strict), au format Source/Rubrique/
   Analyse juridique/Impact opérationnel.
3. On stocke ces fiches dans articles.json (base cumulative, jamais écrasée).
4. On régénère index.html à partir de articles.json avec du code Python
   classique (pas d'IA sur la mise en page -> stable, pas de risque de
   casser le design).

⚠️ À VÉRIFIER avant le premier run : certaines URLs de flux RSS ci-dessous
sont données à titre indicatif (CNIL et CERT-FR confirmés fiables au moment
de l'écriture ; Village Justice / INPI / Legalis / Next à tester et ajuster
si le flux a changé d'adresse — le script est conçu pour ignorer un flux en
erreur sans planter).
"""

import os
import json
import time
import feedparser
from datetime import datetime, timezone
from google import genai
from google.genai import types

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------

ARTICLES_FILE = "articles.json"
OUTPUT_FILE = "index.html"
MAX_ARTICLES_STORED = 200       # taille max de l'historique conservé
MAX_NEW_PER_RUN = 12            # limite d'appels IA par exécution (coût/temps)
MAX_ENTRIES_PER_FEED = 5        # nb d'entrées récentes regardées par flux

CATEGORIES = {
    "Droit de l'IT & Numérique": [
        "https://next.ink/feed/",
        "https://www.legalis.net/feed/",
    ],
    "Cybersécurité": [
        "https://www.cert.ssi.gouv.fr/avis/feed/",
        "https://www.cert.ssi.gouv.fr/alerte/feed/",
    ],
    "Droit des Affaires & Sociétés (SA)": [
        "https://www.village-justice.com/articles/backend.php3",
    ],
    "Fiscalité & Facturation Électronique": [
        "https://www.economie.gouv.fr/rss.xml",
    ],
    "Droit Européen & Compliance (RGPD / AI Act)": [
        "https://www.cnil.fr/fr/rss.xml",
    ],
    "Propriété Intellectuelle (industrielle & intellectuelle)": [
        "https://www.inpi.fr/rss.xml",
    ],
}

PROMPT_TEMPLATE = """Tu es juriste spécialisé en droit des affaires, IP/IT, rattaché à une
direction IT Contract Management dans un groupe industriel (fabricant de câbles,
côté en bourse). Ton lectorat : des gestionnaires de contrats IT (SaaS, Cloud, TMA,
consulting), pas des juristes généralistes.

Voici un article d'actualité juridique brut :
Titre original : {titre}
Source : {source}
Résumé/contenu : {contenu}
Catégorie : {categorie}

Rédige une fiche d'analyse au format STRICT JSON suivant (rien d'autre que le JSON,
pas de balises markdown) :

{{
  "titre": "titre reformulé, clair et professionnel (max 15 mots)",
  "analyse": "3-4 phrases d'analyse juridique factuelle et précise, avec référence
              aux articles de loi/règlement pertinents si identifiables",
  "impact": "2-3 phrases : impact concret pour un gestionnaire de contrats IT
             (clause à ajouter/modifier, point de vigilance dans une négociation
             fournisseur, risque contractuel à anticiper)"
}}

Si l'article n'a aucun rapport exploitable avec le droit des affaires/IT/IA/PI/fiscal,
réponds exactement : {{"skip": true}}
"""

# --------------------------------------------------------------------------
# ÉTAPE 1 — Charger l'historique existant
# --------------------------------------------------------------------------

def load_articles():
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_articles(articles):
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------
# ÉTAPE 2 — Collecter les nouveaux articles depuis les flux RSS
# --------------------------------------------------------------------------

def collect_new_entries(known_links):
    """Parcourt tous les flux et retourne les entrées pas encore connues."""
    new_entries = []
    for categorie, urls in CATEGORIES.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                if feed.bozo and not feed.entries:
                    print(f"⚠️  Flux inaccessible ou invalide, ignoré : {url}")
                    continue
                for entry in feed.entries[:MAX_ENTRIES_PER_FEED]:
                    link = entry.get("link", "")
                    if not link or link in known_links:
                        continue
                    contenu = entry.get("summary", "") or entry.get("description", "")
                    new_entries.append({
                        "categorie": categorie,
                        "titre": entry.get("title", "Sans titre"),
                        "source": feed.feed.get("title", url),
                        "link": link,
                        "contenu": contenu[:1500],  # on tronque, pas besoin de plus
                    })
            except Exception as e:
                print(f"⚠️  Erreur sur le flux {url} : {e}")
                continue
    return new_entries


# --------------------------------------------------------------------------
# ÉTAPE 3 — Générer la fiche d'analyse via Gemini pour chaque nouvel article
# --------------------------------------------------------------------------

def generate_fiche(client, entry):
    prompt = PROMPT_TEMPLATE.format(
        titre=entry["titre"],
        source=entry["source"],
        contenu=entry["contenu"] or "(pas de résumé disponible, base-toi sur le titre)",
        categorie=entry["categorie"],
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        data = json.loads(response.text)
        if data.get("skip"):
            return None
        return {
            "categorie": entry["categorie"],
            "source": entry["source"],
            "link": entry["link"],
            "titre": data["titre"],
            "analyse": data["analyse"],
            "impact": data["impact"],
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
    except Exception as e:
        print(f"⚠️  Erreur de génération pour '{entry['titre']}' : {e}")
        return None


# --------------------------------------------------------------------------
# ÉTAPE 4 — Régénérer index.html à partir de articles.json (pas d'IA ici)
# --------------------------------------------------------------------------

CARD_TEMPLATE = """
<div style="background: white; border-left: 5px solid #c5a059; padding: 1.5rem; border-radius: 0 8px 8px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.8rem; color: #718096; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
        <span>Source : {source}</span>
        <span>{date}</span>
    </div>
    <h3 style="margin: 0 0 0.5rem 0; color: #1a2a3a; font-size: 1.25rem;">{titre}</h3>
    <p style="margin: 0; color: #2d3748;"><b>Analyse juridique :</b> {analyse}</p>
    <div style="background: #f7fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 6px; margin-top: 1rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: #c5a059; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">💼 Impact opérationnel & Pratique Contractuelle</h4>
        <p style="margin: 0; font-size: 0.9rem; color: #4a5568;">{impact}</p>
    </div>
    <a href="{link}" target="_blank" style="font-size: 0.8rem; color: #c5a059;">Source originale →</a>
</div>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Veille Juridique IT, Contrats & IA Act</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; background: #f4f6f8; color: #1a2a3a; }}
  header {{ background: #0d1b2a; color: white; padding: 2.5rem 3rem; border-bottom: 4px solid #c5a059; }}
  header .badge {{ background: #1e2d3f; color: #c5a059; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; }}
  header h1 {{ margin: 0.8rem 0 0.3rem 0; font-size: 2.2rem; }}
  header p {{ color: #a0aec0; margin: 0; }}
  .layout {{ display: flex; max-width: 1400px; margin: 2rem auto; gap: 2rem; padding: 0 2rem; }}
  .sidebar {{ width: 280px; flex-shrink: 0; }}
  .sidebar h2 {{ font-size: 0.9rem; letter-spacing: 0.05em; border-bottom: 2px solid #c5a059; padding-bottom: 0.5rem; }}
  .sidebar a {{ display: block; color: #2d3748; text-decoration: none; padding: 0.4rem 0; font-size: 0.9rem; }}
  .sidebar a:hover {{ color: #c5a059; }}
  main {{ flex: 1; }}
  .category-block {{ margin-bottom: 3rem; }}
  .category-block h2 {{ font-size: 1.4rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.8rem; }}
  .last-update {{ color: #718096; font-size: 0.8rem; text-align: right; max-width: 1400px; margin: 0 auto; padding: 0 2rem; }}
</style>
</head>
<body>
<header>
  <span class="badge">DIRECTION JURIDIQUE &amp; CONTRATS IT</span>
  <h1>Veille Juridique IT, Contrats &amp; IA Act</h1>
  <p>Suivi réglementaire, gouvernance de l'IA et sécurisation des contrats informatiques</p>
</header>
<p class="last-update">Dernière mise à jour automatique : {last_update}</p>
<div class="layout">
  <div class="sidebar">
    <h2>PILIERS RÉGLEMENTAIRES IT</h2>
    {sidebar_links}
  </div>
  <main>
    {category_blocks}
  </main>
</div>
</body>
</html>
"""


def render_html(articles):
    articles_sorted = sorted(articles, key=lambda a: a["date"], reverse=True)
    by_category = {}
    for a in articles_sorted:
        by_category.setdefault(a["categorie"], []).append(a)

    sidebar_links = "\n".join(
        f'<a href="#{cat.replace(" ", "-")}">{cat} ({len(items)})</a>'
        for cat, items in by_category.items()
    )

    category_blocks = ""
    for cat, items in by_category.items():
        cards = "\n".join(CARD_TEMPLATE.format(**item) for item in items)
        category_blocks += f'<div class="category-block" id="{cat.replace(" ", "-")}"><h2>{cat}</h2>{cards}</div>\n'

    html = PAGE_TEMPLATE.format(
        last_update=datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        sidebar_links=sidebar_links,
        category_blocks=category_blocks,
    )
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY n'est pas configurée dans les Secrets GitHub.")

    client = genai.Client(api_key=api_key)

    articles = load_articles()
    known_links = {a["link"] for a in articles}

    print("Recherche de nouveaux articles sur les flux RSS...")
    new_entries = collect_new_entries(known_links)
    print(f"{len(new_entries)} nouvel(le)s entrée(s) détectée(s).")

    new_entries = new_entries[:MAX_NEW_PER_RUN]

    added = 0
    for entry in new_entries:
        fiche = generate_fiche(client, entry)
        if fiche:
            articles.append(fiche)
            added += 1
        time.sleep(1)  # éviter de spammer l'API

    print(f"{added} fiche(s) générée(s) et ajoutée(s).")

    # on garde seulement les N plus récents pour éviter que le fichier grossisse indéfiniment
    articles = sorted(articles, key=lambda a: a["date"], reverse=True)[:MAX_ARTICLES_STORED]

    save_articles(articles)
    render_html(articles)
    print("index.html régénéré avec succès.")


if __name__ == "__main__":
    main()
