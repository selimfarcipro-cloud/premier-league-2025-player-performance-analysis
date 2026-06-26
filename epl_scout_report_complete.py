"""
=============================================================================
EPL SCOUT REPORT 2024-25 - COMPLETE DATA ANALYSIS
=============================================================================
Angle Métier: Identify elite players, undervalued gems, and strategic insights
for recruitment decisions.

Author: Data Analyst Portfolio
Date: 2024-25 Season
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Plotly for interactive visuals
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Statistics & Clustering
from scipy.stats import pearsonr, spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Styling
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("📊 EPL SCOUT REPORT 2024-25 - COMPREHENSIVE ANALYSIS")
print("="*80)

# ============================================================================
# SECTION 1: DATA LOADING & PROFILING
# ============================================================================

print("\n[1] LOADING DATA...")

# Load from Kaggle (adjust path based on your setup)
# For local: df = pd.read_csv('data/raw/epl_player_stats_24_25.csv')
df = pd.read_csv('epl_player_stats_24_25.csv')  # Adjust path

print(f"✓ Dataset shape: {df.shape}")
print(f"✓ Columns: {df.columns.tolist()}\n")

# Display basic info
print("DATASET OVERVIEW:")
print(df.head(3))
print(f"\nDATA TYPES & MISSINGNESS:")
print(df.info())
print(f"\nDESCRIPTIVE STATS:")
print(df.describe().T[['mean', 'std', 'min', 'max']])

# ============================================================================
# SECTION 2: DATA CLEANING & VALIDATION
# ============================================================================

print("\n[2] DATA CLEANING & PREPARATION...")

df = df.copy()

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Convert numeric columns
numeric_cols = ['Goals', 'Assists', 'Minutes', 'Appearances', 'Shots', 
                'Shots On Target', 'Yellow Cards', 'Red Cards', 'Saves', 'xG']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Smart NaN handling
print(f"Missing values BEFORE cleaning:\n{df.isnull().sum()}\n")

# For goals/assists: NaN → 0 (fair assumption)
df[['Goals', 'Assists']] = df[['Goals', 'Assists']].fillna(0)

# For Minutes/Appearances: drop rows with missing core stats
df = df.dropna(subset=['Minutes', 'Appearances'])

# For percentages (e.g., Saves %): use median by position
if 'Saves %' in df.columns:
    gk_median = df[df['Position'] == 'GKP']['Saves %'].median()
    df['Saves %'] = df['Saves %'].fillna(gk_median)

# Fill remaining numeric NaNs with 0 (conservative approach)
df[numeric_cols] = df[numeric_cols].fillna(0)

print(f"Missing values AFTER cleaning:\n{df.isnull().sum()}\n")

# Remove players with 0 appearances (data artifacts)
df = df[df['Appearances'] > 0]

print(f"✓ Dataset cleaned: {df.shape[0]} players remaining\n")

# ============================================================================
# SECTION 3: FEATURE ENGINEERING (Advanced)
# ============================================================================

print("[3] FEATURE ENGINEERING...")

# Per-90-minute normalization (football standard)
df['Goals_per90'] = np.where(df['Minutes'] > 0, (df['Goals'] / df['Minutes']) * 90, 0)
df['Assists_per90'] = np.where(df['Minutes'] > 0, (df['Assists'] / df['Minutes']) * 90, 0)
df['Shots_per90'] = np.where(df['Minutes'] > 0, (df['Shots'] / df['Minutes']) * 90, 0)

# Shot accuracy & conversion
df['Shot_Accuracy'] = np.where(df['Shots'] > 0, 
                               (df['Shots On Target'] / df['Shots']) * 100, 0)
df['Conversion_Rate'] = np.where(df['Shots'] > 0, 
                                  (df['Goals'] / df['Shots']) * 100, 0)

# Discipline metrics
df['Total_Cards'] = df['Yellow Cards'] + (df['Red Cards'] * 2)
df['Cards_per90'] = np.where(df['Minutes'] > 0, 
                              (df['Total_Cards'] / df['Minutes']) * 90, 0)

# Combined performance score
df['Performance_Score'] = (
    (df['Goals_per90'] * 2) +           # Goals weighted 2x
    (df['Assists_per90'] * 1.5) +       # Assists weighted 1.5x
    (df['Shot_Accuracy'] * 0.1)         # Accuracy bonus
)

# Efficiency metrics
df['Playing_Time_Category'] = pd.cut(df['Minutes'], 
                                     bins=[0, 450, 1350, 2700, 5000],
                                     labels=['Reserve', 'Squad Rotation', 'Regular', 'Key Player'])

# Age groups
df['Age_Group'] = pd.cut(df['Age'], 
                         bins=[15, 22, 28, 32, 40],
                         labels=['Young (16-22)', 'Prime (23-28)', 'Experienced (29-32)', 'Veteran (33+)'])

print("✓ Features created:")
print("  - Per-90 minutes normalization (Goals, Assists, Shots)")
print("  - Shot efficiency (Accuracy, Conversion Rate)")
print("  - Discipline metrics (Total Cards, Cards per 90)")
print("  - Performance Score (composite)")
print("  - Playing Time & Age categories\n")

# Display feature engineering results
print("FEATURE ENGINEERING SAMPLE:")
print(df[['Player Name', 'Club', 'Goals_per90', 'Assists_per90', 
          'Performance_Score', 'Playing_Time_Category']].head(10))

# ============================================================================
# SECTION 4: SEGMENTATION & SCOUTING CLASSIFICATION
# ============================================================================

print("\n[4] PLAYER SEGMENTATION (Scout Classification)...")

# Minimum minutes threshold for fair comparison (1 full season)
MIN_MINUTES = 450  # ~5 full matches

df_filtered = df[df['Minutes'] >= MIN_MINUTES].copy()

# Performance tiers
perf_q1 = df_filtered['Performance_Score'].quantile(0.75)
perf_q2 = df_filtered['Performance_Score'].quantile(0.50)
perf_q3 = df_filtered['Performance_Score'].quantile(0.25)

df_filtered['Elite_Tier'] = pd.cut(df_filtered['Performance_Score'],
                                   bins=[0, perf_q3, perf_q2, perf_q1, 1000],
                                   labels=['Below Average', 'Average', 'Above Average', 'Elite'])

# Identify UNDERVALUED players (good performance, low minutes)
df_filtered['Is_Undervalued'] = (
    (df_filtered['Performance_Score'] > df_filtered['Performance_Score'].median()) &
    (df_filtered['Minutes'] < 1350)  # Playing time < regular starter
)

# Identify OVERPERFORMERS (beating xG expectations)
if 'xG' in df.columns and df['xG'].sum() > 0:
    df_filtered['Goals_vs_xG'] = df_filtered['Goals'] - df_filtered['xG']
    df_filtered['Is_Overperformer'] = df_filtered['Goals_vs_xG'] > 3
else:
    df_filtered['Goals_vs_xG'] = 0
    df_filtered['Is_Overperformer'] = False

print("✓ Segmentation complete")
print(f"\nPLAYER DISTRIBUTION BY TIER:")
print(df_filtered['Elite_Tier'].value_counts().sort_index())

# ============================================================================
# SECTION 5: STATISTICAL ANALYSIS & CORRELATIONS
# ============================================================================

print("\n[5] CORRELATION & STATISTICAL ANALYSIS...")

# Select numeric columns for correlation
corr_cols = ['Age', 'Goals', 'Assists', 'Minutes', 'Shots', 'Shot_Accuracy',
             'Goals_per90', 'Assists_per90', 'Performance_Score']
corr_cols = [c for c in corr_cols if c in df.columns]

correlation_matrix = df[corr_cols].corr()

print("TOP CORRELATIONS with Performance_Score:")
perf_corr = correlation_matrix['Performance_Score'].sort_values(ascending=False)
print(perf_corr.head(6))

# Position-wise analysis
print("\nPERFORMANCE BY POSITION:")
position_stats = df_filtered.groupby('Position').agg({
    'Goals_per90': ['mean', 'std', 'count'],
    'Assists_per90': ['mean', 'std'],
    'Performance_Score': ['mean', 'max', 'min'],
    'Minutes': 'mean'
}).round(2)
print(position_stats)

# Age analysis
print("\nPERFORMANCE BY AGE GROUP:")
age_stats = df_filtered.groupby('Age_Group').agg({
    'Performance_Score': ['mean', 'count'],
    'Goals_per90': 'mean',
    'Assists_per90': 'mean',
    'Age': 'mean'
}).round(2)
print(age_stats)

# ============================================================================
# SECTION 6: ELITE PLAYERS IDENTIFICATION
# ============================================================================

print("\n[6] ELITE PLAYERS IDENTIFICATION...")

# Top performers overall
print("\n🏆 TOP 15 ELITE PLAYERS (by Performance Score):")
elite_players = df_filtered.nlargest(15, 'Performance_Score')[
    ['Player Name', 'Club', 'Position', 'Age', 'Goals', 'Assists', 
     'Minutes', 'Performance_Score', 'Elite_Tier']
]
print(elite_players.to_string(index=False))

# By position
print("\n🎯 TOP PERFORMERS BY POSITION:")
for pos in df_filtered['Position'].unique():
    top_pos = df_filtered[df_filtered['Position'] == pos].nlargest(3, 'Performance_Score')
    print(f"\n{pos}:")
    for idx, player in top_pos.iterrows():
        print(f"  • {player['Player Name']} ({player['Club']}) - "
              f"Score: {player['Performance_Score']:.2f}")

# ============================================================================
# SECTION 7: UNDERVALUED & EMERGING TALENT
# ============================================================================

print("\n[7] UNDERVALUED PLAYERS & EMERGING TALENT...")

print("\n💎 UNDERVALUED GEMS (High performance, Low playing time):")
undervalued_df = df_filtered[df_filtered['Is_Undervalued']].nlargest(10, 'Performance_Score')[
    ['Player Name', 'Club', 'Position', 'Age', 'Performance_Score', 'Minutes', 
     'Goals_per90', 'Assists_per90']
]
print(undervalued_df.to_string(index=False))

print("\n🌟 YOUNG TALENTS (Age < 23, Elite tier):")
young_talent = df_filtered[
    (df_filtered['Age'] < 23) & 
    (df_filtered['Elite_Tier'] == 'Elite')
].nlargest(10, 'Performance_Score')[
    ['Player Name', 'Club', 'Position', 'Age', 'Performance_Score', 'Goals_per90']
]
print(young_talent.to_string(index=False))

# ============================================================================
# SECTION 8: CLUSTERING ANALYSIS (Player Archetypes)
# ============================================================================

print("\n[8] CLUSTERING ANALYSIS (Player Archetypes)...")

# Select features for clustering
clustering_features = ['Goals_per90', 'Assists_per90', 'Shot_Accuracy', 'Age']
X_cluster = df_filtered[clustering_features].fillna(0)

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

# K-means (4 clusters = 4 player archetypes)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_filtered['Player_Archetype'] = kmeans.fit_predict(X_scaled)

# Label clusters
archetype_names = {
    0: 'Defensive/Support',
    1: 'Creative Playmaker',
    2: 'Goal Scorer',
    3: 'Versatile Attacker'
}
df_filtered['Player_Archetype'] = df_filtered['Player_Archetype'].map(archetype_names)

print("✓ 4 Player Archetypes identified:")
print(f"\nARCHETYPE DISTRIBUTION:")
print(df_filtered['Player_Archetype'].value_counts())

print("\nARCHETYPE CHARACTERISTICS:")
archetype_stats = df_filtered.groupby('Player_Archetype')[clustering_features].mean().round(2)
print(archetype_stats)

# Top players per archetype
print("\nTOP PLAYERS PER ARCHETYPE:")
for arch in df_filtered['Player_Archetype'].unique():
    top = df_filtered[df_filtered['Player_Archetype'] == arch].nlargest(2, 'Performance_Score')
    print(f"\n{arch}:")
    for _, player in top.iterrows():
        print(f"  • {player['Player Name']} ({player['Club']})")

# ============================================================================
# SECTION 9: CLUB ANALYSIS
# ============================================================================

print("\n[9] CLUB PERFORMANCE ANALYSIS...")

club_stats = df_filtered.groupby('Club').agg({
    'Player Name': 'count',
    'Goals_per90': 'mean',
    'Assists_per90': 'mean',
    'Performance_Score': 'mean',
    'Age': 'mean',
    'Minutes': 'sum'
}).round(2)
club_stats.columns = ['Players', 'Avg_Goals_per90', 'Avg_Assists_per90', 
                      'Avg_Performance', 'Avg_Age', 'Total_Minutes']
club_stats = club_stats.sort_values('Avg_Performance', ascending=False)

print("\nTOP 10 CLUBS BY PERFORMANCE:")
print(club_stats.head(10))

# ============================================================================
# SECTION 10: VISUALIZATION - PLOTLY INTERACTIVE CHARTS
# ============================================================================

print("\n[10] GENERATING INTERACTIVE VISUALIZATIONS...")

# Create output directory
import os
os.makedirs('exports', exist_ok=True)
os.makedirs('visualizations', exist_ok=True)

# -------- CHART 1: Scatter - Performance vs Minutes --------
fig1 = px.scatter(
    df_filtered,
    x='Minutes', y='Performance_Score',
    color='Position', size='Goals_per90',
    hover_name='Player Name',
    hover_data={'Club': True, 'Age': True, 'Goals': True, 'Assists': True},
    title='<b>Player Performance vs Playing Time</b><br><sub>Size = Goals per 90</sub>',
    labels={'Minutes': 'Minutes Played', 'Performance_Score': 'Performance Score'},
    template='plotly_white'
)
fig1.update_layout(width=1200, height=700, hovermode='closest')
fig1.write_html('visualizations/01_performance_vs_minutes.html')
fig1.show()

# -------- CHART 2: Goals vs xG (Overperformance) --------
if df_filtered['xG'].sum() > 0:
    fig2 = px.scatter(
        df_filtered[df_filtered['xG'] > 0],
        x='xG', y='Goals',
        color='Goals_vs_xG',
        size='Minutes',
        hover_name='Player Name',
        hover_data={'Club': True, 'Position': True},
        title='<b>Goals vs Expected Goals (xG)</b><br><sub>Who Over/Underperforms?</sub>',
        template='plotly_white',
        color_continuous_scale='RdYlGn'
    )
    # Add diagonal line (perfect prediction)
    fig2.add_shape(type="line", x0=0, y0=0, x1=30, y1=30, 
                   line=dict(color="gray", width=2, dash="dash"))
    fig2.update_layout(width=1200, height=700)
    fig2.write_html('visualizations/02_goals_vs_xg.html')
    fig2.show()

# -------- CHART 3: Heatmap - Performance by Position --------
position_features = ['Goals_per90', 'Assists_per90', 'Shot_Accuracy', 
                     'Performance_Score', 'Cards_per90']
position_heatmap = df_filtered.groupby('Position')[position_features].mean()

fig3 = go.Figure(data=go.Heatmap(
    z=position_heatmap.values,
    x=position_heatmap.columns,
    y=position_heatmap.index,
    colorscale='Viridis',
    text=np.round(position_heatmap.values, 2),
    texttemplate='%{text:.2f}',
    textfont={"size": 11}
))
fig3.update_layout(
    title='<b>Position Performance Heatmap</b>',
    xaxis_title='Metrics',
    yaxis_title='Position',
    width=1000, height=600
)
fig3.write_html('visualizations/03_position_heatmap.html')
fig3.show()

# -------- CHART 4: Top Players (Bar Chart) --------
top_20 = df_filtered.nlargest(20, 'Performance_Score')
fig4 = px.bar(
    top_20.sort_values('Performance_Score'),
    x='Performance_Score', y='Player Name',
    color='Position',
    hover_data={'Club': True, 'Age': True, 'Goals': True},
    title='<b>Top 20 Elite Players</b>',
    labels={'Performance_Score': 'Performance Score'},
    template='plotly_white'
)
fig4.update_layout(width=1000, height=700)
fig4.write_html('visualizations/04_top_20_players.html')
fig4.show()

# -------- CHART 5: Sunburst - Position → Club → Player --------
fig5 = px.sunburst(
    df_filtered.nlargest(50, 'Performance_Score'),
    path=['Position', 'Club', 'Player Name'],
    values='Performance_Score',
    color='Performance_Score',
    color_continuous_scale='Greens',
    title='<b>Top 50 Players Hierarchy (Position → Club → Player)</b>'
)
fig5.update_layout(width=1000, height=900)
fig5.write_html('visualizations/05_player_hierarchy.html')
fig5.show()

# -------- CHART 6: Player Archetype Distribution --------
archetype_dist = df_filtered.groupby('Player_Archetype').size().reset_index(name='Count')
fig6 = px.pie(
    archetype_dist,
    names='Player_Archetype', values='Count',
    title='<b>Player Archetype Distribution</b>',
    template='plotly_white'
)
fig6.update_traces(textposition='inside', textinfo='percent+label')
fig6.update_layout(width=800, height=600)
fig6.write_html('visualizations/06_archetype_distribution.html')
fig6.show()

# -------- CHART 7: Club Comparison --------
top_clubs = club_stats.head(15)
fig7 = px.bar(
    top_clubs.reset_index(),
    x='Club', y='Avg_Performance',
    color='Avg_Goals_per90',
    title='<b>Top 15 Clubs by Average Player Performance</b>',
    labels={'Avg_Performance': 'Avg Performance Score'},
    template='plotly_white',
    color_continuous_scale='Blues'
)
fig7.update_layout(xaxis_tickangle=-45, width=1200, height=600)
fig7.write_html('visualizations/07_club_comparison.html')
fig7.show()

# -------- CHART 8: Age vs Performance --------
fig8 = px.scatter(
    df_filtered,
    x='Age', y='Performance_Score',
    color='Position', size='Minutes',
    hover_name='Player Name',
    hover_data={'Club': True, 'Goals_per90': ':.2f'},
    title='<b>Age vs Performance</b><br><sub>Size = Minutes Played</sub>',
    template='plotly_white'
)
fig8.update_layout(width=1200, height=700)
fig8.write_html('visualizations/08_age_vs_performance.html')
fig8.show()

# -------- CHART 9: Undervalued Players --------
if df_filtered['Is_Undervalued'].sum() > 0:
    undervalued_top = df_filtered[df_filtered['Is_Undervalued']].nlargest(15, 'Performance_Score')
    fig9 = px.scatter(
        undervalued_top,
        x='Minutes', y='Performance_Score',
        color='Position', size='Goals_per90',
        hover_name='Player Name',
        hover_data={'Club': True, 'Age': True},
        title='<b>Undervalued Players (High Performance, Low Minutes)</b>',
        template='plotly_white'
    )
    fig9.update_layout(width=1000, height=700)
    fig9.write_html('visualizations/09_undervalued_players.html')
    fig9.show()

# ============================================================================
# SECTION 11: DATA EXPORTS FOR POWER BI
# ============================================================================

print("\n[11] EXPORTING DATA FOR POWER BI...")

# Export 1: Full player data with all metrics
export_full = df_filtered[[
    'Player Name', 'Club', 'Position', 'Age', 'Age_Group',
    'Goals', 'Assists', 'Minutes', 'Appearances',
    'Goals_per90', 'Assists_per90', 'Shot_Accuracy', 'Conversion_Rate',
    'Performance_Score', 'Elite_Tier', 'Player_Archetype',
    'Is_Undervalued', 'Is_Overperformer', 'Goals_vs_xG',
    'Total_Cards', 'Cards_per90'
]].copy()

export_full = export_full.sort_values('Performance_Score', ascending=False)
export_full.to_csv('exports/01_players_full_stats.csv', index=False, encoding='utf-8-sig')
print("✓ Exported: 01_players_full_stats.csv")

# Export 2: Scout Report (Top prospects)
scout_report = export_full[export_full['Elite_Tier'] == 'Elite'].head(50)
scout_report.to_csv('exports/02_scout_report_elite.csv', index=False, encoding='utf-8-sig')
print("✓ Exported: 02_scout_report_elite.csv")

# Export 3: Undervalued Players
undervalued_export = export_full[export_full['Is_Undervalued']].head(30)
undervalued_export.to_csv('exports/03_undervalued_gems.csv', index=False, encoding='utf-8-sig')
print("✓ Exported: 03_undervalued_gems.csv")

# Export 4: Young Talents
young_talents_export = export_full[(export_full['Age'] < 23) & 
                                    (export_full['Elite_Tier'] == 'Elite')]
young_talents_export.to_csv('exports/04_young_talents.csv', index=False, encoding='utf-8-sig')
print("✓ Exported: 04_young_talents.csv")

# Export 5: Club Summary
club_export = club_stats.reset_index()
club_export.to_csv('exports/05_club_summary.csv', index=False, encoding='utf-8-sig')
print("✓ Exported: 05_club_summary.csv")

# Export 6: Position Analysis
position_export = df_filtered.groupby('Position').agg({
    'Player Name': 'count',
    'Goals_per90': ['mean', 'median', 'std', 'max'],
    'Assists_per90': ['mean', 'median', 'std', 'max'],
    'Performance_Score': ['mean', 'median', 'max'],
    'Age': 'mean',
    'Minutes': 'mean'
}).reset_index()
position_export.to_csv('exports/06_position_analysis.csv', index=False, encoding='utf-8-sig')
print("✓ Exported: 06_position_analysis.csv")

print("\n✅ All exports saved to 'exports/' folder\n")

# ============================================================================
# SECTION 12: SUMMARY & KEY INSIGHTS
# ============================================================================

print("="*80)
print("📋 SCOUT REPORT SUMMARY - KEY INSIGHTS")
print("="*80)

print("\n🏆 ELITE INSIGHTS:")
print(f"  • Total Elite Players: {(export_full['Elite_Tier'] == 'Elite').sum()}")
print(f"  • Top Performer: {export_full.iloc[0]['Player Name']} ({export_full.iloc[0]['Club']}) - Score: {export_full.iloc[0]['Performance_Score']:.2f}")
print(f"  • Highest Goals/90: {df_filtered.loc[df_filtered['Goals_per90'].idxmax(), 'Player Name']} ({df_filtered['Goals_per90'].max():.2f})")
print(f"  • Highest Assists/90: {df_filtered.loc[df_filtered['Assists_per90'].idxmax(), 'Player Name']} ({df_filtered['Assists_per90'].max():.2f})")

print("\n💎 RECRUITMENT OPPORTUNITIES:")
print(f"  • Undervalued Players Found: {df_filtered['Is_Undervalued'].sum()}")
print(f"  • Young Talents (U-23): {((df_filtered['Age'] < 23) & (df_filtered['Elite_Tier'] == 'Elite')).sum()}")
if df_filtered['Is_Overperformer'].sum() > 0:
    print(f"  • Overperformers (vs xG): {df_filtered['Is_Overperformer'].sum()}")

print("\n📊 POSITION BREAKDOWN:")
for pos in df_filtered['Position'].unique():
    pos_data = df_filtered[df_filtered['Position'] == pos]
    print(f"  • {pos}: {len(pos_data)} players | Avg Score: {pos_data['Performance_Score'].mean():.2f}")

print("\n🔗 CLUB STRENGTH:")
top_3_clubs = club_stats.head(3)
for club in top_3_clubs.index:
    print(f"  • {club}: {top_3_clubs.loc[club, 'Avg_Performance']:.2f} avg performance")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE - All exports ready for Power BI")
print("="*80)
