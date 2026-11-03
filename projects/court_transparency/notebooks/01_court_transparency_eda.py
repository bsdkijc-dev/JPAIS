import pandas as pd
import numpy as np

df = pd.read_csv('data/scorecard.csv')
print('=== INDONESIAN COURT TRANSPARENCY SCORECARD ===')
print(f'Total Courts: {len(df)}')
print(df[['court_name', 'jurisdiction', 'clearance_rate', 'publication_rate', 'openness_index']])
print('
Mean Openness Index by Jurisdiction:')
print(df.groupby('jurisdiction')['openness_index'].mean())
