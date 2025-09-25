import psycopg2                 # Import psycopg2 for PostgreSQL connection
import pandas as pd             # Import pandas for data manipulation

# ---------------------------
# Database connection
# ---------------------------
# Replace these with your PostgreSQL credentials
host = "localhost"
port = 5432
user = "postgres"
password = "20000324"
database = "spotify_bi"

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
cursor = conn.cursor()
print("Connected to PostgreSQL database:", database)

# ---------------------------
# Step 2: Create tables
# ---------------------------

# Drop tables if they exist (clean start)
cursor.execute("DROP TABLE IF EXISTS fact_user_activity;")
cursor.execute("DROP TABLE IF EXISTS dim_device;")
cursor.execute("DROP TABLE IF EXISTS dim_subscription;")
cursor.execute("DROP TABLE IF EXISTS dim_user;")
conn.commit()

# 2a: dim_user
cursor.execute("""
CREATE TABLE dim_user (
    user_id INT PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    age_group VARCHAR(10),
    country VARCHAR(50)
);
""")

# 2b: dim_subscription
cursor.execute("""
CREATE TABLE dim_subscription (
    subscription_type VARCHAR(20) PRIMARY KEY,
    subscription_flag INT
);
""")

# 2c: dim_device
cursor.execute("""
CREATE TABLE dim_device (
    device_type VARCHAR(20) PRIMARY KEY
);
""")

# 2d: fact_user_activity
cursor.execute("""
CREATE TABLE fact_user_activity (
    user_id INT REFERENCES dim_user(user_id),
    listening_time INT,
    songs_played_per_day INT,
    skip_rate FLOAT,
    ads_listened_per_week INT,
    offline_listening INT,
    engagement_score INT,
    high_skip_user INT,
    subscription_type VARCHAR(20) REFERENCES dim_subscription(subscription_type),
    device_type VARCHAR(20) REFERENCES dim_device(device_type),
    is_churned INT
);
""")

conn.commit()
print("Tables created successfully.")

# ---------------------------
# Step 3: Load CSVs into PostgreSQL
# ---------------------------

# Load CSVs
dim_user_df = pd.read_csv("../data/dim_user.csv")
dim_subscription_df = pd.read_csv("../data/dim_subscription.csv")
dim_device_df = pd.read_csv("../data/dim_device.csv")
fact_df = pd.read_csv("../data/fact_user_activity.csv")

# Helper function to insert DataFrame into table
def insert_dataframe(df, table_name):
    for i, row in df.iterrows():
        # Build SQL placeholders
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    conn.commit()
    print(f"Inserted {len(df)} rows into {table_name}")

# Insert dimension tables first
insert_dataframe(dim_user_df, 'dim_user')
insert_dataframe(dim_subscription_df, 'dim_subscription')
insert_dataframe(dim_device_df, 'dim_device')

# Then insert fact table
insert_dataframe(fact_df, 'fact_user_activity')

# ---------------------------
# Step 4: Test sample join
# ---------------------------
cursor.execute("""
SELECT f.user_id, f.engagement_score, u.age_group, s.subscription_type, d.device_type
FROM fact_user_activity f
JOIN dim_user u ON f.user_id = u.user_id
JOIN dim_subscription s ON f.subscription_type = s.subscription_type
JOIN dim_device d ON f.device_type = d.device_type
LIMIT 5;
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

# ---------------------------
# Step 5: Close connection
# ---------------------------
cursor.close()
conn.close()
print("PostgreSQL connection closed.")
