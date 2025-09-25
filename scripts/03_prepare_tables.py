# 03_prepare_tables.py

import pandas as pd

# ---------------------------
# Load cleaned dataset
# ---------------------------
clean_file = "../data/spotify_cleaned.csv"
df = pd.read_csv(clean_file)
print("Cleaned dataset loaded. Shape:", df.shape)

# ---------------------------
# Create dimension tables
# ---------------------------

# Dimension table for users
# Includes descriptive info about the user
# This is useful for dashboard filters and joins in SQL
dim_user = df[['user_id', 'gender', 'age', 'age_group', 'country']].drop_duplicates()
print("dim_user shape:", dim_user.shape)
print(dim_user.head())

# Dimension table for subscriptions
# Maps subscription_type to a flag (Free=0, Paid=1)
# Keeps it separate for aggregation by subscription type
dim_subscription = df[['subscription_type', 'subscription_flag']].drop_duplicates()
print("dim_subscription shape:", dim_subscription.shape)
print(dim_subscription.head())

# Dimension table for device types
# Simple table for joining device info in fact table
dim_device = df[['device_type']].drop_duplicates()
print("dim_device shape:", dim_device.shape)
print(dim_device.head())

# ---------------------------
# Create fact table
# ---------------------------
# Fact table stores all numeric metrics and foreign keys for analysis
# Connects to dimension tables using IDs or descriptive fields

fact_user_activity = df[['user_id',
                         'listening_time',
                         'songs_played_per_day',
                         'skip_rate',
                         'ads_listened_per_week',
                         'offline_listening',
                         'engagement_score',
                         'high_skip_user',
                         'subscription_type',  # will join with dim_subscription
                         'device_type',        # will join with dim_device
                         'is_churned']]

print("fact_user_activity shape:", fact_user_activity.shape)
print(fact_user_activity.head())

# ---------------------------
# Save tables for next step (PostgreSQL insertion)
# ---------------------------
dim_user.to_csv("../data/dim_user.csv", index=False)
dim_subscription.to_csv("../data/dim_subscription.csv", index=False)
dim_device.to_csv("../data/dim_device.csv", index=False)
fact_user_activity.to_csv("../data/fact_user_activity.csv", index=False)

print("All dimension and fact tables saved as CSVs for DB loading.")
