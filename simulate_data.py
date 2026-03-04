"""
simulate_data.py
----------------
ROOTKey A/B Test — Data Simulation Script

This script generates a plausible simulated dataset for the ROOTKey
landing page A/B test. Parameters are anchored to real observations:

  - Version A (control):   ~10% conversion rate (from company data)
  - Version B (treatment): ~16% conversion rate (hypothesised uplift)
  - Traffic split:          3:1 (A:B) — as observed in the real test
  - Total visitors:         1,000 (realistic for a 2-week newsletter campaign
                            with ~200k subscribers and ~0.5% CTR)

Secondary/guiderail metrics (time on page, bounce rate) are also
simulated to reflect the expected improvement from Version B's
reduced friction and cleaner CTA hierarchy.

Output: rootkey_ab_data.csv
"""

import numpy as np
import pandas as pd

# ── Random seed for reproducibility ──────────────────────────────────────────
np.random.seed(42)

# ── Experiment parameters ─────────────────────────────────────────────────────
N_TOTAL = 1000          # total visitors
SPLIT   = 0.5         # proportion going to version A 

N_A = int(N_TOTAL * SPLIT)   
N_B = N_TOTAL - N_A           

# Conversion rates (binary outcome: signed up or not)
P_CONVERT_A = 0.10   # baseline: ~10% (from real company observation)
P_CONVERT_B = 0.16   # treatment: ~16% (hypothesised ~60% relative uplift)

# Guiderail: time on page (seconds)
# Version B expected to increase engagement due to demo CTA + social proof order
TIME_MEAN_A, TIME_SD_A = 45, 20
TIME_MEAN_B, TIME_SD_B = 62, 22

# Guiderail: bounce rate
# Version B expected to reduce bounces due to cleaner CTA hierarchy
BOUNCE_P_A = 0.58
BOUNCE_P_B = 0.48

# ── Simulate version A ────────────────────────────────────────────────────────
df_A = pd.DataFrame({
    'visitor_id':        range(1, N_A + 1),
    'variant':           'A',
    'converted':         np.random.binomial(1, P_CONVERT_A, N_A),
    'time_on_page_sec':  np.random.normal(TIME_MEAN_A, TIME_SD_A, N_A).clip(5, 300).round(1),
    'bounce':            np.random.binomial(1, BOUNCE_P_A, N_A),
})

# ── Simulate version B ────────────────────────────────────────────────────────
df_B = pd.DataFrame({
    'visitor_id':        range(N_A + 1, N_TOTAL + 1),
    'variant':           'B',
    'converted':         np.random.binomial(1, P_CONVERT_B, N_B),
    'time_on_page_sec':  np.random.normal(TIME_MEAN_B, TIME_SD_B, N_B).clip(5, 300).round(1),
    'bounce':            np.random.binomial(1, BOUNCE_P_B, N_B),
})

# ── Combine and shuffle ───────────────────────────────────────────────────────
df = pd.concat([df_A, df_B], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle rows

# ── Save ──────────────────────────────────────────────────────────────────────
output_path = 'rootkey_ab_data.csv'
df.to_csv(output_path, index=False)

print(f"Dataset saved to: {output_path}")
print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumn descriptions:")
print(f"  visitor_id        — unique visitor identifier")
print(f"  variant           — 'A' (control) or 'B' (treatment)")
print(f"  converted         — 1 if visitor signed up, 0 otherwise (PRIMARY KPI)")
print(f"  time_on_page_sec  — seconds spent on landing page (guiderail)")
print(f"  bounce            — 1 if visitor left without any interaction (guiderail)")
print(f"\nGroup sizes:")
print(df['variant'].value_counts().to_string())
print(f"\nSimulation parameters:")
print(f"  Conversion rate A: {P_CONVERT_A*100:.0f}%  |  Conversion rate B: {P_CONVERT_B*100:.0f}%")
print(f"  Traffic split:     {SPLIT*100:.0f}% / {(1-SPLIT)*100:.0f}%  (A / B)")
