# Crypto Data Pipeline & BI Dashboard

## Présentation du projet

Ce projet consiste à concevoir une pipeline de données permettant de collecter, transformer, stocker et visualiser des données de cryptomonnaies.

Les données sont récupérées depuis une API publique (CoinGecko), stockées dans DuckDB, transformées avec dbt, orchestrées avec Dagster et visualisées via un dashboard interactif développé avec Streamlit.

---

## Choix de conception

Le projet repose sur les technologies suivantes :

- **Dagster** : orchestration de la pipeline, gestion des assets et monitoring des exécutions (runs, logs, erreurs)
- **DuckDB** : base de données analytique légère pour le stockage des données
- **dbt (Data Build Tool)** : transformation des données et création de tables analytiques
- **Streamlit** : création du dashboard BI interactif
- **pytest** : tests unitaires pour garantir la fiabilité du pipeline
+ **scikit-learn** : implémentation du modèle de Machine Learning pour la prédiction

---

## Architecture

```text
API Crypto
   ↓
Dagster Asset : crypto_prices_raw
   ↓
DuckDB : crypto_prices_raw
   ↓
dbt : daily_summary, moving_averages
   ↓
Streamlit Dashboard
```

---

## 📁 Arborescence du projet

```text
dagster-crypto-pipeline/
│
├── dagster_pipeline/              ← package principal Dagster
│   ├── __init__.py
│   ├── definitions.py             ← point d’entrée Dagster
│   ├── jobs.py                    ← définition des jobs
│   ├── schedules.py               ← planification
│   ├── sensors.py                 ← déclencheurs
│   ├── assets/
│   │   ├── __init__.py
│   │   ├── extract.py             ← extraction API CoinGecko
│   │   └── dbt_assets.py          ← intégration dbt
│   └── resources/
│       ├── __init__.py
│       └── database.py            ← connexion DuckDB
│
├── dbt_project/                  ← projet dbt
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_prices.sql
│   │   └── marts/
│   │       ├── daily_summary.sql
│   │       └── moving_averages.sql
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── dashboard/                    ← application Streamlit
│   └── app.py
│
├── tests/                        ← tests pytest
│   ├── __init__.py
│   ├── test_extract.py
│   └── test_transforms.py
│
├── data/                         ← base DuckDB (non versionnée)
├── logs/                         ← logs de la pipeline
├── triggers/                     ← fichiers de déclenchement
│
├── check_db.py                   ← vérification des données
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```
---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/chifa376/dagster-crypto-pipeline.git
cd dagster-crypto-pipeline
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l’environnement (Windows)

```bash
.venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Exécuter la pipeline

### 1. Lancer l’extraction des données

```bash
python -c "from dagster_pipeline.assets.extract import crypto_prices_raw; crypto_prices_raw()"
```

### 2. Lancer les transformations dbt

```bash
cd dbt_project/crypto_pipeline
dbt run
cd ../..
```

### 3. Vérifier les données

```bash
python check_db.py
```

---

## Lancer Dagster

```bash
dagster dev
```

Puis ouvrir :

```text
http://127.0.0.1:3000
```

Dagster permet de suivre :
- les runs
- les statuts (Success / Failure)
- les logs
- les erreurs
- les assets

---

## Lancer le dashboard Streamlit

```bash
streamlit run dashboard/app.py
```

Le dashboard contient :
- KPI crypto
- graphiques de prix
- analyse du Market Cap
- tendances
- filtres crypto et temps
- recommandations BI

---

## Machine Learning & Prédiction

Une fonctionnalité de prédiction a été intégrée afin d’apporter une analyse avancée des données.

### Objectif

Prédire l’évolution du prix des cryptomonnaies à court terme et fournir une aide à la décision basée sur les tendances du marché.

### Méthode utilisée

- Modèle : **Régression Linéaire (Linear Regression)**
- Données utilisées :
  - historique des prix
  - timestamps d’extraction
- Entraînement : en temps réel à partir des données disponibles

### Fonctionnalités

- Prédiction du prochain prix
- Calcul de la variation attendue (%)
- Comparaison entre prix réel et prix prédit
- Visualisation graphique (courbe réelle vs prédite)

### Indicateur "Market Mood"

Un indicateur intelligent est calculé pour qualifier l’état du marché :

- 🟢 Momentum positif → tendance haussière
- 🟡 Marché stable → faible variation
- 🟠 Marché volatil → forte fluctuation
- 🔴 Correction → tendance baissière

### Interprétation BI

Le système génère automatiquement une interprétation basée sur :

- la variation sur 24h
- la position du prix par rapport à la moyenne mobile
- la tendance globale

---

## Tests

### Lancer les tests unitaires

```bash
python -m pytest
```

### Les tests vérifient :

- l’extraction des données
- la création de la table brute
- l’existence des tables transformées
- la qualité des données

---

## Monitoring

Le monitoring est assuré à deux niveaux :

### Logs applicatifs

Des logs ont été ajoutés dans le code pour :
- suivre l’exécution de la pipeline
- afficher les données extraites
- détecter les erreurs

### Dagster

Dagster permet de :
- visualiser les runs
- voir les statuts (success / failure)
- consulter les logs
- suivre les assets

### En cas d’erreur

- le pipeline passe en échec
- les logs facilitent le débogage

---

## Auteurs

Projet réalisé par :

- Chifa CHOUCHANE  
- Yasmine BEN-HAJ-SALAH  
- Cyrine CHAMMEM  

---

## Conclusion

Ce projet met en place une pipeline de données complète combinant extraction, transformation, stockage, visualisation et monitoring, répondant aux exigences d’un système décisionnel moderne.