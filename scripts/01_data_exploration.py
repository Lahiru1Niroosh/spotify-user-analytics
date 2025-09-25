# 01_data_exploration.py

import pandas as pd                         # Import pandas for data manipulation
import matplotlib.pyplot as plt             # Import visualization libraries
import seaborn as sns                       # for enhanced visualizations



# Load the dataset
file_path = "../data/spotify_churn.csv"  
df = pd.read_csv(file_path)

# Quick peek at the data
print("Shape of the dataset (rows, columns):", df.shape)
print("\nColumn names:\n", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())

# Check data types
print("\nData types of each column:\n", df.dtypes)

# Check for missing values
print("\nMissing values per column:\n", df.isnull().sum())

# Check for duplicates
duplicates = df.duplicated().sum()
print("\nNumber of duplicate rows:", duplicates)

# Basic statistics for numeric columns
print("\nNumeric column statistics:\n", df.describe())

# Distribution of target variable
print("\nChurn distribution (0 = active, 1 = churned):\n", df['is_churned'].value_counts(normalize=True))

# Set seaborn style for nicer plots
sns.set(style="whitegrid")


# -------------------------------
# Numeric Columns Exploration
# -------------------------------

numeric_cols = ['age', 'listening_time', 'songs_played_per_day', 'skip_rate', 'ads_listened_per_week', 'offline_listening']

# Histograms for numeric columns
for col in numeric_cols:
    plt.figure(figsize=(8,4))
    sns.histplot(df[col], bins=20, kde=True, color='skyblue')
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.show()

# Boxplots to spot outliers
for col in numeric_cols:
    plt.figure(figsize=(8,4))
    sns.boxplot(x=df[col], color='lightgreen')
    plt.title(f'Boxplot of {col}')
    plt.show()

# -------------------------------
# Categorical Columns Exploration
# -------------------------------

categorical_cols = ['gender', 'country', 'subscription_type', 'device_type']

# Count plots for categorical columns
for col in categorical_cols:
    plt.figure(figsize=(8,4))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index, palette='Set2')
    plt.title(f'Count of {col}')
    plt.xticks(rotation=45)
    plt.show()

# -------------------------------
# Churn vs Categorical Columns 
# -------------------------------

for col in categorical_cols:
    plt.figure(figsize=(8,4))
    sns.countplot(data=df, x=col, hue='is_churned', palette='Set1')
    plt.title(f'Churn vs {col}')
    plt.xticks(rotation=45)
    plt.show()

# -------------------------------
# Correlation heatmap for numeric columns
# -------------------------------

plt.figure(figsize=(10,6))
sns.heatmap(df[numeric_cols + ['is_churned']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()


