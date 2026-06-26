# ⚡ QUICK START - 5 MINUTES

## 1️⃣ TÉLÉCHARGE LE DATASET

Kaggle URL:  
https://www.kaggle.com/datasets/aesika/english-premier-league-player-stats-2425

Télécharge le CSV: `epl_player_stats_24_25.csv`

---

## 2️⃣ INSTALLE LES DÉPENDANCES

```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn scipy
```

---

## 3️⃣ LANCE L'ANALYSE

### Option A: Jupyter Notebook (Recommandé - Interactif)
```bash
jupyter notebook epl_scout_report.ipynb
```
- Ouvre le notebook dans le navigateur
- Lance les cellules dans l'ordre
- Change le chemin du CSV si nécessaire (ligne 1 du code)
- Visualise les charts interactifs inline
- Vois les exports CSV dans le dossier `exports/`

### Option B: Python Script (Direct - Moins de config)
```bash
python epl_scout_report_complete.py
```
- Exécute l'analyse complète
- Génère tous les exports automatiquement
- Affiche les résultats dans le terminal

---

## 4️⃣ RÉSULTATS

Après l'exécution, tu auras:

```
📊 visualizations/
   ├── 01_performance_vs_minutes.html
   ├── 02_goals_vs_xg.html
   ├── 03_position_heatmap.html
   ├── 04_top_20_players.html
   ├── 05_player_hierarchy.html
   ├── 06_archetype_distribution.html
   ├── 07_club_comparison.html
   ├── 08_age_vs_performance.html
   └── 09_undervalued_players.html

📈 exports/ (pour Power BI)
   ├── 01_players_full_stats.csv
   ├── 02_scout_report_elite.csv
   ├── 03_undervalued_gems.csv
   ├── 04_young_talents.csv
   ├── 05_club_summary.csv
   └── 06_position_analysis.csv
```

---

## 5️⃣ POINTS CLÉS DU CODE

### Si ton dataset a des colonnes différentes:

Cherche dans le code:
```python
numeric_cols = ['Goals', 'Assists', 'Minutes', ...]
```
Change les noms pour matcher ton dataset.

### Pour ajuster les seuils:

```python
MIN_MINUTES = 450  # Change si tu veux (ex: 1000)
df_filtered = df[df['Minutes'] >= MIN_MINUTES].copy()
```

### Pour modifier le Performance Score:

```python
df['Performance_Score'] = (
    (df['Goals_per90'] * 2) +      # Change le poids ici
    (df['Assists_per90'] * 1.5) +  # ou ici
    (df['Shot_Accuracy'] * 0.1)    # ou là
)
```

---

## 6️⃣ PROCHAINES ÉTAPES

✅ **Power BI Dashboard**
- Importe les CSVs de `exports/`
- Crée des visualisations

✅ **GitHub**
- Push sur `selimfarcipro-cloud/epl-scout-report`

✅ **Portfolio (Notion)**
- Crée une page avec insights clés
- Embed les charts HTML

---

## ❓ PROBLÈMES COURANTS

**"FileNotFoundError: epl_player_stats_24_25.csv"**  
→ Change le chemin dans la première cellule de code

**"ModuleNotFoundError: No module named 'plotly'"**  
→ Installe: `pip install plotly`

**"Columns don't match"**  
→ Affiche `df.columns.tolist()` et ajuste les noms

**"Division by zero"**  
→ Déjà géré (np.where conditions)

---

## 📊 CE QUE TU VAS APPRENDRE

✅ Per-90-minute normalization en football analytics  
✅ Smart data cleaning vs naive fillna()  
✅ K-Means clustering pour segmentation  
✅ Plotly interactive charts production-ready  
✅ Power BI workflow (Python → CSV → Dashboard)  
✅ Business angle métier (decision-focused analysis)

---

## 🚀 BON COURAGE !

C'est un projet **production-ready** avec:
- ✅ Code professionnel
- ✅ Analyse avancée
- ✅ Visualisations interactives
- ✅ Exports Power BI
- ✅ Documentation complète

**Durée estimée**: 15-20 min pour tourner + 1h pour explorer les résultats

**Pour des questions**: Vois le README.md complet
