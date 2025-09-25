# 02_data_cleaning.py
import pandas as pd

# Load raw CSV
file_path = "../data/spotify_churn.csv"
df = pd.read_csv(file_path)

# ---------------------------
# Step 1: Clean categorical columns
# ---------------------------
df['gender'] = df['gender'].str.strip().str.capitalize()
df['subscription_type'] = df['subscription_type'].str.strip().str.capitalize()
df['device_type'] = df['device_type'].str.strip().str.capitalize()

# ---------------------------
# Step 2: Feature engineering
# ---------------------------
bins = [15, 25, 35, 45, 60]
labels = ['16-25','26-35','36-45','46-60']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

df['engagement_score'] = df['listening_time'] + df['songs_played_per_day']
df['high_skip_user'] = (df['skip_rate'] > 0.5).astype(int)
df['subscription_flag'] = df['subscription_type'].apply(lambda x: 0 if x=='Free' else 1)

# ---------------------------
# Step 3: Save cleaned CSV for next step
# ---------------------------
clean_file = "../data/spotify_cleaned.csv"
df.to_csv(clean_file, index=False)
print(f"Cleaned dataset saved to {clean_file}")
