# %% [markdown]
# # Gaming Industry Sales Analysis - Step-by-Step Python Project
#
# **Goal:** Clean a raw gaming sales dataset, analyze revenue, create charts,
# and export the cleaned data.
#
# **Before you start:** keep `gaming_sales_raw.csv` in the same folder as this file.
# (If it is missing, run `python make_dataset.py` first.)
#
# **Install packages if needed:** `pip install pandas numpy matplotlib`
#
# **How to run in VS Code:** install the "Python" and "Jupyter" extensions, then
# click "Run Cell" above any `# %%` block, or just run the file:
# `python gaming_industry_analysis.py`
#
# Note: the data is practice data (synthetic), not real company sales figures.

# %% [markdown]
# ## Step 1 - Import libraries
# Pandas handles tabular data, NumPy handles numbers, Matplotlib creates charts.

# %%
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Make Python look for files in the same folder as this script,
# no matter which folder VS Code was opened in.
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass  # running in a notebook/interactive cell: already in the right folder

os.makedirs("charts", exist_ok=True)

# %% [markdown]
# ## Step 2 - Load the CSV file
# Run this cell and check that the file is in the same folder.

# %%
df = pd.read_csv("gaming_sales_raw.csv", dtype={"Order_ID": str})

print("Dataset loaded successfully")
print("Rows and columns:", df.shape)
print(df.head())

# %% [markdown]
# ## Step 3 - Understand the dataset
# Inspect column names, data types, missing values, and summary statistics.

# %%
print("Column names:")
print(df.columns.tolist())          # a LIST of column names

print("\nData types and non-null counts:")
df.info()

print("\nSummary statistics:")
print(df.describe(include="all"))

print("\nMissing values by column:")
print(df.isnull().sum())

# %% [markdown]
# ## Step 4 - Check duplicate records
# Count exact duplicate rows before removing them.

# %%
duplicate_count = df.duplicated().sum()
print("Exact duplicate rows:", duplicate_count)

# %% [markdown]
# ## Step 5 - Remove exact duplicates
# Keep the first occurrence of each fully identical row.

# %%
df = df.drop_duplicates().copy()
print("Shape after removing duplicates:", df.shape)

# %% [markdown]
# ## Step 6 - Clean text columns
# Remove leading/trailing spaces and fix capitalization.
#
# Why not just use `.str.title()`? It would turn `PC` into `Pc` and `GTA V`
# into `Gta V`. So we use a **tuple** of correct names and a **dictionary**
# that maps the lowercase version of each name to its proper spelling.

# %%
VALID_NAMES = (   # tuple: fixed list of correct spellings that should not change
    "North", "South", "East", "West",
    "PC", "PlayStation", "Xbox", "Nintendo", "Mobile",
    "RPG", "Sports", "Shooter", "Sandbox", "Action", "Racing",
    "Adventure", "Battle Royale",
    "Elden Ring", "FIFA 25", "Call of Duty", "Minecraft", "GTA V",
    "Forza Horizon 5", "Zelda Tears Kingdom", "BGMI Elite Pass",
    "Valorant Points", "Genshin Impact Pack",
    "Sony", "Microsoft", "EA", "Activision", "Krafton",
)

# dictionary comprehension: {"pc": "PC", "gta v": "GTA V", ...}
canonical = {name.lower(): name for name in VALID_NAMES}

text_columns = ["Region", "Game", "Genre", "Platform", "Publisher"]   # a list

for column in text_columns:                       # loop over the list
    cleaned = df[column].astype("string").str.strip()
    df[column] = cleaned.str.lower().map(canonical).fillna(cleaned)

print(df[text_columns].head(10))

# %% [markdown]
# ## Step 7 - Correct data types
# Convert dates and numeric columns. Values that cannot be converted become
# missing (`NaT` or `NaN`).

# %%
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Units"] = pd.to_numeric(df["Units"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

print(df.dtypes)

# %% [markdown]
# ## Step 8 - Identify invalid values
# For this practice dataset, units and unit price must be positive.
# Treat non-positive values as invalid (set them to missing).

# %%
df.loc[df["Units"] <= 0, "Units"] = np.nan
df.loc[df["Unit_Price"] <= 0, "Unit_Price"] = np.nan

print("Missing values after conversion and validation:")
print(df.isnull().sum())

# %% [markdown]
# ## Step 9 - Handle missing values
# Order date, region, game, units, and unit price are essential for calculating
# sales, so remove rows missing these fields. A missing publisher is kept and
# labelled `Unknown`.

# %%
rows_before = len(df)

essential_columns = ("Order_Date", "Region", "Game", "Units", "Unit_Price")  # tuple
df = df.dropna(subset=list(essential_columns)).copy()

df["Units"] = df["Units"].astype(int)
df["Publisher"] = df["Publisher"].fillna("Unknown")

print("Rows removed:", rows_before - len(df))
print("Rows remaining:", len(df))
print(df.isnull().sum())

# %% [markdown]
# ## Step 10 - Create a revenue column
# Revenue for each order line = units x unit price.

# %%
df["Revenue"] = df["Units"] * df["Unit_Price"]
print(df.head())

# %% [markdown]
# ## Step 11 - Calculate key business metrics
# Answer: total revenue, unique orders, units sold, and average revenue per order.
# NumPy is used for the median and the 90th percentile.

# %%
total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Units"].sum()
average_order_revenue = df.groupby("Order_ID")["Revenue"].sum().mean()
median_revenue = np.median(df["Revenue"])
p90_revenue = np.percentile(df["Revenue"], 90)

print(f"Total revenue: Rs {total_revenue:,.2f}")
print(f"Unique orders: {total_orders}")
print(f"Units sold: {total_units}")
print(f"Average revenue per order: Rs {average_order_revenue:,.2f}")
print(f"Median order-line revenue: Rs {median_revenue:,.2f}")
print(f"Top 10% order lines are above: Rs {p90_revenue:,.2f}")

# %% [markdown]
# ## Step 12 - Analyze revenue by region
# `groupby()` groups rows by region, and `sum()` adds the revenue in each group.

# %%
region_sales = (
    df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)
print("Top region:", region_sales.idxmax())

# %% [markdown]
# ## Step 13 - Analyze revenue by game
# Find which game generated the most revenue and which sold the most units.

# %%
game_revenue = (
    df.groupby("Game")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

game_units = (
    df.groupby("Game")["Units"]
    .sum()
    .sort_values(ascending=False)
)

print("Revenue by game:")
print(game_revenue)
print("\nUnits by game:")
print(game_units)
print("\nTop revenue game:", game_revenue.idxmax())
print("Top units game:", game_units.idxmax())

# %% [markdown]
# ## Step 14 - Analyze platform and genre (extra gaming analysis)
# These two views are specific to the gaming industry.

# %%
platform_sales = df.groupby("Platform")["Revenue"].sum().sort_values(ascending=False)
genre_sales = df.groupby("Genre")["Revenue"].sum().sort_values(ascending=False)

total = platform_sales.sum()
print("Revenue share by platform:")
for platform, value in platform_sales.items():        # loop over a Series
    share = value / total * 100
    print(f"  {platform:<12} Rs {value:>10,.0f}  ({share:.1f}%)")

print("\nTop 3 genres:")
for rank, (genre, value) in enumerate(genre_sales.head(3).items(), start=1):
    print(f"  {rank}. {genre}: Rs {value:,.0f}")

# %% [markdown]
# ## Step 15 - Analyze monthly sales
# Extract the month from the order date and aggregate revenue.

# %%
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("Month")["Revenue"].sum().sort_index()
print(monthly_sales)
print("Best month:", monthly_sales.idxmax())

# %% [markdown]
# ## Step 16 - Label sales tiers with NumPy
# Use `np.where` (an if/else for a whole column) to flag big orders.

# %%
df["Sale_Tier"] = np.where(df["Revenue"] >= p90_revenue, "High", "Normal")
print(df["Sale_Tier"].value_counts())

# %% [markdown]
# ## Step 17 - Visualize revenue by region
# A bar chart makes regional comparisons easier.

# %%
region_sales.plot(kind="bar", title="Revenue by Region", ylabel="Revenue (Rs)")
plt.xlabel("Region")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/revenue_by_region.png", dpi=120)
plt.show()

# %% [markdown]
# ## Step 18 - Visualize revenue by game

# %%
game_revenue.sort_values().plot(kind="barh", title="Revenue by Game", xlabel="Revenue (Rs)")
plt.ylabel("Game")
plt.tight_layout()
plt.savefig("charts/revenue_by_game.png", dpi=120)
plt.show()

# %% [markdown]
# ## Step 19 - Visualize platform share and monthly trend

# %%
platform_sales.plot(kind="pie", autopct="%1.1f%%", title="Revenue Share by Platform")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/platform_share.png", dpi=120)
plt.show()

monthly_sales.plot(kind="line", marker="o", title="Monthly Revenue Trend", ylabel="Revenue (Rs)")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_trend.png", dpi=120)
plt.show()

# %% [markdown]
# ## Step 20 - Export the cleaned data

# %%
df.to_csv("gaming_sales_cleaned.csv", index=False)

summary = pd.DataFrame({
    "Metric": ["Total revenue", "Unique orders", "Units sold",
               "Average revenue per order", "Top region", "Top game by revenue",
               "Top game by units", "Top platform", "Top genre", "Best month"],
    "Value": [f"{total_revenue:,.2f}", total_orders, total_units,
              f"{average_order_revenue:,.2f}", region_sales.idxmax(),
              game_revenue.idxmax(), game_units.idxmax(),
              platform_sales.idxmax(), genre_sales.idxmax(), monthly_sales.idxmax()],
})
summary.to_csv("gaming_summary.csv", index=False)
print("Export complete!")

# %% [markdown]
# ## Step 21 - Student interpretation
# Write 4-5 business observations in your own words. Questions to answer:
#
# 1. Which region generated the highest revenue?
# 2. Which game generated the highest revenue?
# 3. Which game sold the most units? Is it the same game as question 2? Why or why not?
# 4. Which platform and genre earn the most?
# 5. Which month had the highest revenue?
# 6. What data-quality problems were found, and how were they handled?
#
# **Important:** The cleaning choices here are teaching assumptions. In a real
# project, confirm business rules with the data owner before deleting records.

# %%
# Auto-generated answers to check your own observations against:
print("1. Top region:", region_sales.idxmax(), f"(Rs {region_sales.max():,.0f})")
print("2. Top revenue game:", game_revenue.idxmax(), f"(Rs {game_revenue.max():,.0f})")
print("3. Top units game:", game_units.idxmax(), f"({game_units.max()} units)")
print("4. Top platform:", platform_sales.idxmax(), "| Top genre:", genre_sales.idxmax())
print("5. Best month:", monthly_sales.idxmax(), f"(Rs {monthly_sales.max():,.0f})")
