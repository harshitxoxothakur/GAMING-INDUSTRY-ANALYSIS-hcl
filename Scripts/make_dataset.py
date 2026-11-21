"""
make_dataset.py
Creates gaming_sales_raw.csv: a PRACTICE dataset (synthetic, not real sales data)
with deliberate data-quality problems, like the retail sample your trainer gave.
Run once:  python make_dataset.py
"""
import random
import csv

random.seed(42)

# (game, genre, platform, base price in INR)
CATALOG = [
    ("Elden Ring",          "RPG",       "PC",          3999),
    ("FIFA 25",             "Sports",    "PlayStation", 4499),
    ("Call of Duty",        "Shooter",   "Xbox",        4999),
    ("Minecraft",           "Sandbox",   "PC",          1999),
    ("GTA V",               "Action",    "PlayStation", 2499),
    ("Forza Horizon 5",     "Racing",    "Xbox",        3499),
    ("Zelda Tears Kingdom", "Adventure", "Nintendo",    5999),
    ("BGMI Elite Pass",     "Battle Royale", "Mobile",   799),
    ("Valorant Points",     "Shooter",   "PC",           999),
    ("Genshin Impact Pack", "RPG",       "Mobile",      1499),
]
REGIONS = ["North", "South", "East", "West"]
PUBLISHERS = ["Sony", "Microsoft", "Nintendo", "EA", "Activision", "Krafton"]

rows = []
for i in range(1, 58):
    game, genre, platform, price = random.choice(CATALOG)
    month = random.randint(1, 10)
    day = random.randint(1, 28)
    rows.append([
        f"{i:04d}",
        f"2026-{month:02d}-{day:02d}",
        random.choice(REGIONS),
        game, genre, platform,
        random.randint(1, 12),
        price,
        random.choice(PUBLISHERS),
    ])

# ---- inject realistic data-quality problems (for the cleaning steps) ----
rows[3][2]  = "north"                 # wrong capitalisation
rows[7][2]  = "  West "               # extra spaces
rows[11][3] = "  minecraft"           # spaces + lowercase
rows[15][5] = "pc "                   # trailing space, lowercase
rows[19][6] = ""                      # missing units
rows[23][6] = "two"                   # text instead of number
rows[27][7] = -1999                   # negative price (invalid)
rows[31][6] = 0                       # zero units (invalid)
rows[35][1] = "not available"         # bad date
rows[39][8] = ""                      # missing publisher
rows[43][2] = ""                      # missing region
rows.append(list(rows[5]))            # exact duplicate row
rows.append(list(rows[20]))           # exact duplicate row

header = ["Order_ID", "Order_Date", "Region", "Game", "Genre",
          "Platform", "Units", "Unit_Price", "Publisher"]

with open("gaming_sales_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"gaming_sales_raw.csv created with {len(rows)} rows")
