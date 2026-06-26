# 🏆 EPL SCOUT REPORT 2024-25

## Complete Data Analysis & Player Identification System

**Version**: 1.0  
**Dataset**: English Premier League 2024-25 Season  
**Angle Métier**: Elite player identification, undervalued gem discovery, strategic recruitment insights  

---

## 📋 Project Overview

This comprehensive data analysis project identifies:
- **Elite Players** → Top performers by position and overall performance
- **Undervalued Gems** → High performance players with limited playing time
- **Young Talents** → Emerging prospects under 23 with elite-tier performance
- **Player Archetypes** → 4 distinct player clusters (Goal Scorer, Playmaker, etc.)
- **Club Insights** → Team composition and squad strength analysis

**Key Deliverables**:
✅ Python Jupyter Notebook (fully commented)  
✅ 9 Interactive Plotly visualizations  
✅ 6 Power BI-ready CSV exports  
✅ Advanced statistical analysis (correlations, clustering)  
✅ Business-focused insights (recruitment, strategy)

---

## 🎯 Key Features

### 1. **Advanced Feature Engineering**
```
- Per-90-minute normalization (Goals/90, Assists/90)
- Shot efficiency metrics (Accuracy %, Conversion Rate)
- Discipline analysis (Cards per 90)
- Performance Score (composite metric: 2×Goals + 1.5×Assists + 0.1×Accuracy)
- Age & Playing Time categorization
```

### 2. **Smart Player Segmentation**
```
- Elite Tier Classification (Elite, Above Average, Average, Below Average)
- Undervalued Players Detection (High performance + Low minutes)
- Overperformer Identification (vs xG expectations)
- K-Means Clustering (4 Player Archetypes)
```

### 3. **Statistical Insights**
```
- Correlation analysis (Performance factors)
- Position-based performance breakdown
- Age group analysis
- Club performance ranking
- Overperformance metrics (Goals vs xG)
```

### 4. **Interactive Visualizations** (Plotly)
```
1. Performance vs Playing Time (Bubble scatter)
2. Goals vs xG Analysis (Overperformance detection)
3. Position Performance Heatmap
4. Top 20 Elite Players (Bar chart)
5. Player Hierarchy (Sunburst chart)
6. Archetype Distribution (Pie chart)
7. Club Comparison (Performance ranking)
8. Age vs Performance (Trend analysis)
9. Undervalued Players (Discovery)
```

### 5. **Power BI Ready Exports**
```
📊 01_players_full_stats.csv
   → All players with all metrics (Power BI main table)

🏆 02_scout_report_elite.csv
   → Top 50 elite players (recruitment focus)

💎 03_undervalued_gems.csv
   → High performance, low minutes (bargain opportunities)

🌟 04_young_talents.csv
   → Elite players under 23 (future investments)

🏢 05_club_summary.csv
   → Club-level aggregates (team analysis)

📍 06_position_analysis.csv
   → Position-specific statistics (role benchmarking)
```

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn scipy
```

### Running the Analysis

**Option 1: Jupyter Notebook (Recommended)**
```bash
jupyter notebook epl_scout_report.ipynb
```
- Run cells sequentially
- Modify paths as needed
- View interactive Plotly charts inline

**Option 2: Python Script**
```bash
python epl_scout_report_complete.py
```
- Runs full analysis end-to-end
- Outputs all visualizations to `visualizations/` folder
- Exports all CSV files to `exports/` folder

---

## 📁 Project Structure

```
epl-scout-report/
│
├── epl_scout_report.ipynb              # Main Jupyter notebook
├── epl_scout_report_complete.py        # Standalone Python script
├── README.md                            # This file
│
├── data/
│   ├── raw/
│   │   └── epl_player_stats_24_25.csv  # Original dataset (Kaggle)
│   └── processed/
│       └── (cleaned data)
│
├── exports/                            # Power BI ready CSVs
│   ├── 01_players_full_stats.csv
│   ├── 02_scout_report_elite.csv
│   ├── 03_undervalued_gems.csv
│   ├── 04_young_talents.csv
│   ├── 05_club_summary.csv
│   └── 06_position_analysis.csv
│
├── visualizations/                     # Interactive Plotly charts
│   ├── 01_performance_vs_minutes.html
│   ├── 02_goals_vs_xg.html
│   ├── 03_position_heatmap.html
│   ├── 04_top_20_players.html
│   ├── 05_player_hierarchy.html
│   ├── 06_archetype_distribution.html
│   ├── 07_club_comparison.html
│   ├── 08_age_vs_performance.html
│   └── 09_undervalued_players.html
│
└── [Your local working directory]
```

---

## 📊 Key Metrics Explained

### Performance Score (Composite)
```
Performance_Score = (Goals_per90 × 2) + (Assists_per90 × 1.5) + (Shot_Accuracy × 0.1)

Why this weighting?
- Goals (2x): Primary output metric in football
- Assists (1.5x): Creative contribution (second priority)
- Accuracy (0.1x): Efficiency bonus (tertiary)
```

### Goals vs xG (Expected Goals)
```
Goals_vs_xG = Actual_Goals - Expected_Goals

Interpretation:
- Positive value: Overperformer (converts well)
- Negative value: Underperformer (misses chances)
- Range: -5 to +5 considered significant
```

### Player Archetype Clusters
```
1. Goal Scorer
   → High Goals/90, Medium Assists/90, High Shot Accuracy
   
2. Creative Playmaker
   → Medium Goals/90, High Assists/90, Varied Accuracy
   
3. Defensive/Support
   → Low Goals/90, Low Assists/90, Age variance
   
4. Versatile Attacker
   → Balanced Goals & Assists, Consistent performance
```

---

## 🔍 How to Use Exports in Power BI

### Import Strategy
1. Open Power BI Desktop
2. **Home** → **Get Data** → **CSV**
3. Load all 6 CSVs (one at a time)
4. **Transform Data** → Ensure data types are correct
5. Create relationships:
   - `Player Name` (main table) ← connects to → all dimension tables

### Recommended Dashboard Structure

**Page 1: Scout Overview**
- KPI Cards: Elite count, Avg Performance, Top player
- Scatter: Performance vs Minutes (by position)
- Table: Top 20 players (Name, Club, Score, Goals/90)
- Filter: Position, Club, Age Group

**Page 2: Position Analysis**
- Heatmap: Position × Performance metrics
- Bar: Top performers per position
- Table: Position benchmarks (avg stats)
- Filter: Position dropdown

**Page 3: Talent Hunt**
- Table: Undervalued players
- Table: Young talents (U-23)
- Pie: Archetype distribution
- Scatter: Age vs Performance

---

## 📈 Analysis Methodology

### Data Cleaning Strategy
✓ Column name cleaning (whitespace removal)  
✓ Numeric type conversion (coerce to numeric)  
✓ Smart NaN handling:
  - Goals/Assists: Fill with 0 (fair assumption)
  - Minutes: Drop if missing (core metric)
  - Position-specific stats: Fill with position median
✓ Remove players with 0 appearances (data artifacts)

### Minimum Thresholds
- **Playing time filter**: 450+ minutes (~5 full matches)
- **Ratio calculations**: Only if denominator > 0
- **Age consideration**: Valid range 15-40 years

### Feature Engineering Sequence
1. Per-90 normalization (core)
2. Efficiency metrics (shots, accuracy)
3. Discipline analysis (cards)
4. Composite scoring (Performance Score)
5. Categorization (Age, Playing Time)
6. Segmentation (Elite Tier, Undervalued, Overperformer)
7. Clustering (K-Means, 4 archetypes)

---

## 🎓 Learning Outcomes

After completing this project, you'll understand:

✅ **Data Analysis Foundation**
- Per-90-minute normalization in sports analytics
- Smart missing data handling vs naive fillna()
- Feature engineering for composite metrics

✅ **Statistical Analysis**
- Correlation analysis and interpretation
- Outlier handling in sports data
- Position-based performance benchmarking

✅ **Advanced Techniques**
- K-Means clustering for player segmentation
- Standardization/scaling in ML pipelines
- Overperformance metrics (vs expected values)

✅ **Visualization & Communication**
- Plotly interactive charts (business presentation)
- Data story telling (angle métier)
- Multiple visualization types (scatter, heatmap, sunburst)

✅ **Portfolio Skills**
- End-to-end analysis (raw → insights → export)
- Code organization and documentation
- CSV export for BI tools (Power BI workflow)

---

## 🔧 Customization Guide

### Change Minimum Playing Time Threshold
```python
MIN_MINUTES = 450  # Change this value
df_filtered = df[df['Minutes'] >= MIN_MINUTES].copy()
```

### Adjust Performance Score Weights
```python
df['Performance_Score'] = (
    (df['Goals_per90'] * 3) +        # Increase weight for goals
    (df['Assists_per90'] * 1) +      # Decrease weight for assists
    (df['Shot_Accuracy'] * 0.05)     # Modify accuracy bonus
)
```

### Modify Clustering
```python
kmeans = KMeans(n_clusters=5, random_state=42)  # 5 archetypes instead of 4
```

### Change Visualization Colors/Templates
```python
fig = px.scatter(..., template='plotly_dark')  # Change theme
color_continuous_scale='Blues'  # Change color scheme
```

---

## ❓ FAQ

**Q: Why use Per-90-minute metrics?**  
A: Football standard. Normalizes for different playing time (2 players, 90 min vs 180 min).

**Q: What if xG column is missing?**  
A: Code handles this gracefully (sets Is_Overperformer to False).

**Q: How to adjust elite tier thresholds?**  
A: Modify quantile values (0.75, 0.50, 0.25).

**Q: Can I use different clustering features?**  
A: Yes, modify `clustering_features` list (ensure same number of features).

**Q: How to export for different BI tools (Looker, Tableau)?**  
A: CSVs are tool-agnostic. Process same as Power BI.

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Dataset not found  
**Solution**: Check file path in `pd.read_csv('path/to/file.csv')`

**Issue**: Plotly charts not displaying  
**Solution**: Ensure plotly installed (`pip install plotly`)

**Issue**: Missing column errors  
**Solution**: Check column names match your dataset (may vary by Kaggle version)

**Issue**: Memory error on large dataset  
**Solution**: Filter to specific clubs/seasons before analysis

---

## 📚 References & Resources

### Football Analytics Best Practices
- Per-90 normalization standard in football
- xG (Expected Goals) interpretation
- Player archetype clustering methodology

### Libraries Used
- **Pandas**: Data manipulation & aggregation
- **NumPy**: Numerical operations
- **Plotly**: Interactive visualizations
- **Scikit-learn**: K-Means clustering, StandardScaler
- **SciPy**: Statistical functions (correlation)

### Kaggle Dataset
**English Premier League - Player Stats - 24/25**  
https://www.kaggle.com/datasets/aesika/english-premier-league-player-stats-2425

---

## 📄 License & Attribution

This analysis is designed for portfolio, educational, and non-commercial use.

**Data Source**: Kaggle - English Premier League  
**Analysis**: Data Analyst Portfolio Project  
**Created**: 2024-25 Season  

---

## 🚀 Next Steps

### To Enhance This Project:

1. **Add Time Series Analysis**
   - Track player performance across matchweeks
   - Injury impact assessment
   - Form trends

2. **Advanced ML Models**
   - Predict player value/salary
   - Season performance forecasting
   - Player injury risk scoring

3. **Interactive Dashboard**
   - Power BI multi-page dashboard
   - Real-time data refresh (if API available)
   - Custom KPI metrics

4. **Comparative Analysis**
   - Season-over-season trends
   - League comparison (EPL vs La Liga, etc.)
   - Historical benchmarking

5. **Database Integration**
   - PostgreSQL backend
   - dbt data transformations
   - BigQuery for scalability

---

## ✅ Checklist for Portfolio Presentation

- [x] Clean, production-ready code
- [x] Comprehensive documentation
- [x] Advanced feature engineering
- [x] Statistical analysis
- [x] Multiple visualization types
- [x] Business-focused insights (not just reporting)
- [x] Power BI-ready exports
- [x] README with clear instructions
- [x] Code comments explaining key decisions
- [x] Reproducible analysis workflow

---

**Status**: ✅ Complete & Ready for Portfolio  
**GitHub**: Push to `selimfarcipro-cloud/epl-scout-report`  
**Notion**: Document findings in portfolio showcase

---

**Questions?** Check the [FAQ](#faq) section or review code comments in the notebook.

**Happy Analyzing! ⚽📊**
