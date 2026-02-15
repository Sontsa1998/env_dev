# 🚗⚡ Tableau de Bord Analytique des Véhicules Électriques

## 📋 Présentation du Projet

Ce projet est une application web interactive développée avec **Streamlit** qui permet d'analyser les données des véhicules électriques. L'application offre une interface conviviale pour explorer les performances des véhicules électriques à travers quatre indicateurs clés de performance (KPI) distincts.

### Objectifs Principaux

1. **Lecture des données CSV** : Charger les données du fichier `electric_vehicles_spec_2025.csv`
2. **Stockage avec DuckDB** : Stocker et interroger les données localement avec DuckDB
3. **Visualisations interactives** : Afficher quatre KPI différents avec des visualisations pertinentes
4. **Filtrage dynamique** : Filtrer les résultats par marque, segment et type de carrosserie

## 🎯 Fonctionnalités

### 1. Chargement des Données
- Interface de téléchargement de fichier CSV
- Validation et chargement automatique dans DuckDB
- Affichage du nombre de véhicules chargés

### 2. Filtrage Dynamique
- **Filtre par Marque** : Sélectionner une ou plusieurs marques
- **Filtre par Segment** : Filtrer par catégorie de véhicule
- **Filtre par Type de Carrosserie** : Choisir le type de carrosserie (Sedan, SUV, Hatchback, etc.)
- Logique **AND** : Tous les filtres s'appliquent simultanément

### 3. Quatre Indicateurs Clés (KPI)

#### KPI 1 : Plage Moyenne par Segment
- **Visualisation** : Graphique en barres
- **Données** : Autonomie moyenne (km) pour chaque segment
- **Utilité** : Comparer l'autonomie entre les différents segments

#### KPI 2 : Accélération Moyenne par Marque
- **Visualisation** : Graphique en barres
- **Données** : Temps d'accélération 0-100 km/h moyen par marque
- **Utilité** : Comparer les performances d'accélération entre marques

#### KPI 3 : Capacité Batterie vs Efficacité Énergétique
- **Visualisation** : Graphique de dispersion (scatter plot)
- **Données** : Relation entre capacité batterie (kWh) et efficacité (Wh/km)
- **Couleurs** : Différenciation par segment
- **Utilité** : Identifier les corrélations entre batterie et efficacité

#### KPI 4 : Distribution par Type de Carrosserie
- **Visualisation** : Graphique en camembert (pie chart)
- **Données** : Nombre et pourcentage de véhicules par type
- **Utilité** : Comprendre la composition du dataset

## 🛠️ Technologies Utilisées

- **Streamlit** : Framework pour l'interface web interactive
- **DuckDB** : Base de données SQL embarquée pour le stockage et les requêtes
- **Pandas** : Manipulation et analyse des données
- **Plotly** : Visualisations interactives
- **Python 3.8+** : Langage de programmation

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le dépôt** (ou télécharger les fichiers)
```bash
git clone <url-du-depot>
cd ev-analytics-dashboard
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancer l'Application

```bash
streamlit run main.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Workflow Typique

1. **Charger les données**
   - Cliquez sur "Charger les données"
   - Sélectionnez le fichier `electric_vehicles_spec_2025.csv`
   - Cliquez sur "Charger les données"

2. **Appliquer les filtres** (optionnel)
   - Utilisez la barre latérale pour sélectionner les filtres
   - Les visualisations se mettent à jour automatiquement

3. **Explorer les KPI**
   - Consultez les quatre visualisations dans la grille 2x2
   - Survolez les graphiques pour voir les détails

4. **Réinitialiser**
   - Cliquez sur "Effacer les données" pour recommencer
   - Cliquez sur "Actualiser" pour rafraîchir l'affichage

## 📊 Structure des Données

Le fichier CSV contient les colonnes suivantes :

| Colonne | Type | Description |
|---------|------|-------------|
| brand | VARCHAR | Marque du véhicule |
| model | VARCHAR | Modèle du véhicule |
| top_speed_kmh | DECIMAL | Vitesse maximale (km/h) |
| battery_capacity_kWh | DECIMAL | Capacité batterie (kWh) |
| battery_type | VARCHAR | Type de batterie |
| number_of_cells | INTEGER | Nombre de cellules |
| torque_nm | DECIMAL | Couple moteur (Nm) |
| efficiency_wh_per_km | DECIMAL | Efficacité énergétique (Wh/km) |
| range_km | DECIMAL | Autonomie (km) |
| acceleration_0_100_s | DECIMAL | Accélération 0-100 km/h (s) |
| fast_charging_power_kw_dc | DECIMAL | Puissance charge rapide (kW) |
| fast_charge_port | VARCHAR | Type de port de charge |
| towing_capacity_kg | DECIMAL | Capacité de remorquage (kg) |
| cargo_volume_l | DECIMAL | Volume de cargo (litres) |
| seats | INTEGER | Nombre de sièges |
| drivetrain | VARCHAR | Type de transmission |
| segment | VARCHAR | Segment du véhicule |
| length_mm | DECIMAL | Longueur (mm) |
| width_mm | DECIMAL | Largeur (mm) |
| height_mm | DECIMAL | Hauteur (mm) |
| car_body_type | VARCHAR | Type de carrosserie |
| source_url | VARCHAR | URL source des données |

## 🧪 Tests Unitaires

### Exécuter les Tests

```bash
pytest tests/ -v
```

### Exécuter les Tests avec Couverture

```bash
pytest tests/ --cov=src --cov-report=html
```

### Structure des Tests

- **test_database.py** : Tests du module de base de données
  - Chargement CSV
  - Requêtes avec filtres
  - Calculs des KPI
  - Gestion des données

- **test_filters.py** : Tests du module de filtrage
  - Récupération des filtres disponibles
  - Application des filtres
  - Résumés des filtres

- **test_visualizations.py** : Tests du module de visualisations
  - Génération des graphiques
  - Gestion des données vides
  - Validation des titres

## 📁 Structure du Projet

```
ev-analytics-dashboard/
├── src/
│   ├── __init__.py
│   ├── app.py                 # Application Streamlit principale
│   ├── database.py            # Gestion DuckDB
│   ├── filters.py             # Gestion des filtres
│   └── visualizations.py      # Moteur de visualisations
├── tests/
│   ├── __init__.py
│   ├── test_database.py       # Tests de la base de données
│   ├── test_filters.py        # Tests des filtres
│   └── test_visualizations.py # Tests des visualisations
├── main.py                    # Point d'entrée
├── requirements.txt           # Dépendances Python
├── README.md                  # Ce fichier
└── electric_vehicles_spec_2025.csv  # Données
```

## 👥 Répartition des Tâches (Équipe de 4)

### Membre 1 : Architecture et Base de Données
- Conception de l'architecture générale
- Implémentation du module `database.py`
- Configuration de DuckDB et des schémas
- Tests unitaires pour la base de données

### Membre 2 : Interface Utilisateur
- Développement de l'application Streamlit (`app.py`)
- Mise en page et design de l'interface
- Gestion des états de session
- Intégration des composants

### Membre 3 : Visualisations et Filtres
- Implémentation du module `visualizations.py`
- Création des quatre KPI
- Développement du module `filters.py`
- Tests des visualisations et filtres

### Membre 4 : Tests et Documentation
- Écriture des tests unitaires complets
- Documentation du code
- Rédaction du README
- Validation et assurance qualité

## 🔧 Configuration Avancée

### Variables d'Environnement

Aucune variable d'environnement requise pour le fonctionnement de base.

### Personnalisation

Pour modifier les filtres disponibles, éditez la méthode `get_available_filters()` dans `src/filters.py`.

## 🐛 Dépannage

### L'application ne démarre pas
```bash
# Vérifier que Streamlit est installé
pip install streamlit

# Vérifier la version de Python
python --version
```

### Erreur lors du chargement du CSV
- Vérifiez que le fichier CSV a le bon format
- Assurez-vous que toutes les colonnes requises sont présentes
- Vérifiez l'encodage du fichier (UTF-8 recommandé)

### Les visualisations ne s'affichent pas
- Vérifiez que les données sont chargées
- Vérifiez que les filtres ne sont pas trop restrictifs
- Essayez de réinitialiser avec le bouton "Effacer les données"

## 📈 Améliorations Futures

- [ ] Export des données filtrées en CSV
- [ ] Graphiques supplémentaires (histogrammes, heatmaps)
- [ ] Comparaison de deux segments
- [ ] Analyse de tendances temporelles
- [ ] Authentification utilisateur
- [ ] Sauvegarde des filtres favoris

## 📝 Licence

Ce projet est fourni à titre éducatif.

## 📞 Support

Pour toute question ou problème, veuillez consulter la documentation ou contacter l'équipe de développement.

---

**Dernière mise à jour** : 2024
**Version** : 1.0.0
**Statut** : Production
