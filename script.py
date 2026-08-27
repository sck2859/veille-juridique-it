import os
import google.generativeai as genai

# 1. Connexion sécurisée à l'IA avec la clé secrète
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY n'est pas configurée dans les Secrets GitHub.")

genai.configure(api_key=api_key)

# 2. La matière brute universitaire pour alimenter le mémoire
base_donnees_fiscales = """
- Source: [BOFiP - Doctrine Administrative]. Régime des micro-BNC et créateurs de contenu sur les plateformes de streaming (Twitch, YouTube). Clarification sur l'articulation entre l'abattement forfaitaire de 34% et les dépenses réelles (frais de matériel, setup, serveurs). Seuil de basculement au régime réel et gestion des redevances de droits d'auteur.
- Source: [Conseil d'État - Jurisprudence]. Arrêt CE, 15 mars 2026. Qualification des revenus issus d'abonnements directs étrangers (OnlyFans, Patreon, Substack). Les gains sont qualifiés de bénéfices non commerciaux (BNC) professionnels dès lors que l'activité est exercée à titre habituel, entraînant l'application de la retenue à la source et le contrôle des flux financiers transfrontaliers.
- Source: [CJUE - Jurisprudence]. Territorialité de la TVA sur les services numériques de divertissement. Analyse de l'assujettissement à la TVA européenne pour les placements de produits, sponsorings transfrontaliers et abonnements B2C. Obligation d'immatriculation au guichet unique (OSS) dès le premier euro.
- Source: [Dalloz - Revue de Droit Fiscal]. La requalification fiscale des avantages en nature accordés aux influenceurs. Étude approfondie sur l'article 79 du Code général des impôts (CGI) et le risque de redressement fiscal lorsque des créateurs omettent de déclarer la valeur marchande des cadeaux, vêtements de luxe ou séjours offerts en échange de visibilité.
- Source: [Navis / Editions Francis Lefebvre - Doctrine]. Structuration sociétaire des créateurs de contenu : Arbitrage entre Entreprise Individuelle (EI) et SASU. Analyse d'impact sur l'optimisation fiscale des revenus des streamers, comparaison des taux effectifs d'imposition (IR vs IS) et risques de requalification en abus de droit.
- Source: [Légifrance - Textes de Lois]. Projet de Loi de Finances - Renforcement des contrôles sur l'économie des plateformes numériques. Obligations de transmission automatique des revenus par les plateformes au fisc français pour harmoniser le contrôle de la fraude fiscale sur les revenus numériques.
"""

# 3. Brief de l'IA : elle doit générer le site EN ENTIER avec les fiches à l'intérieur
consigne_ia = f"""
Tu es un avocat fiscaliste de haut niveau et directeur de recherche en droit fiscal numérique. 
Tu dois générer un site web Toolkit intégral, moderne et parfaitement structuré en HTML pour un mémoire universitaire intitulé : "Le régime fiscal des créateurs de contenu".

Génère la page HTML complète en te basant RIGOUREUSEMENT sur ces informations : {base_donnees_fiscales}.
Tu dois classer chaque source dans sa bonne catégorie et rédiger une fiche d'analyse universitaire détaillée.

Renvoie le code HTML complet de la page en intégrant le CSS directement dans une balise <style> dans le <head> pour éviter tout problème d'affichage.

Voici la structure exacte du design que tu dois respecter :
- Un bandeau de titre (header) sombre avec une bordure dorée/or.
- Une mise en page en deux colonnes : à gauche, une barre latérale (sidebar) affichant la "Structure du Mémoire" (Partie 1 : Qualification des revenus, Partie 2 : Fiscalité indirecte et internationale).
- À droite, le flux principal divisé en 3 grandes sections académiques très claires :
    1. ⚖️ Jurisprudence & Contentieux (Conseil d'État, CJUE)
    2. 📜 Doctrine Administrative & Textes (BOFiP, Lois)
    3. 📚 Doctrine Universitaire & Revues (Dalloz, Navis)

Chaque fiche d'analyse juridique à l'intérieur de ces conteneurs doit obligatoirement ressembler à ça :
<div style="background: white; border-left: 5px solid #c5a059; padding: 1.5rem; border-radius: 0 8px 8px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.8rem; color: #718096; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
        <span>Source : NOM_DE_LA_SOURCE</span>
        <span>Statut : Analyse Académique</span>
    </div>
    <h3 style="margin: 0 0 0.5rem 0; color: #1a2a3a; font-size: 1.25rem;">TITRE_PRECIS_DE_L_ARTICLE</h3>
    <p style="margin: 0; color: #2d3748;"><b>Résumé de la position :</b> UN_RESUME_JURIDIQUE_DEVELOPPE_ET_PROFESSIONNEL_D_ENVIRON_4_LIGNES</p>
    <div style="background: #f7fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 6px; margin-top: 1rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: #c5a059; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">💡 Apport pour la rédaction du Mémoire</h4>
        <p style="margin: 0; font-size: 0.9rem; color: #4a5568;">EXPLICATION_STRATEGIQUE_POUR_L_ETUDIANTE_POUR_INTEGRER_CELA_DANS_SON_PLAN_ET_SON_ARGUMENTATION</p>
    </div>
</div>

Règles impératives : 
- Remplis les catégories avec TOUTES les fiches correspondantes de la base de données brute.
- Renvoie UNIQUEMENT le code HTML complet de la page. Ne mets AUCUNE balise de bloc de code (comme ```html au début ou ``` à la fin). Démarre directement à <!DOCTYPE html>.
"""

print("Génération du Toolkit complet par l'IA Gemini...")

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(consigne_ia)
    
    html_content = response.text.strip()
    
    # Nettoyage des balises markdown si l'IA en ajoute
    if html_content.startswith("```html"):
        html_content = html_content[7:]
    elif html_content.startswith("```"):
        html_content = html_content[3:]
    if html_content.endswith("```"):
        html_content = html_content[:-3]
    html_content = html_content.strip()

    # Écriture dans index.html
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)
        
    print("Succès ! Le Toolkit a été généré dans index.html.")

except Exception as e:
    print(f"Une erreur est survenue : {e}")
    
