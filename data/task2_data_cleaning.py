import pandas as pd  # pandas is the main data-handling library

# 1. List of raw input CSV files (adjust names if needed)
input_files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv",
]

# We will collect cleaned DataFrames from each file in this list
cleaned_frames = []

for file_path in input_files:
    # 2. Read one CSV into a DataFrame
    df = pd.read_csv(file_path)

    # 3. Filter to only Pink Morsels
    df["product"] = df["product"].str.lower()
    df_pink = df[df["product"].isin(["pink morsel"])].copy()

    # 4. Clean and convert 'quantity' and 'price' to numeric
    df_pink["quantity"] = pd.to_numeric(df_pink["quantity"], errors="coerce")

    df_pink["price"] = (
        df_pink["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.strip()
    )
    df_pink["price"] = pd.to_numeric(df_pink["price"], errors="coerce")

    df_pink["sales"] = df_pink["quantity"] * df_pink["price"]

    # 5. Build a new DataFrame with only Sales, Date, Region
    df_formatted = df_pink[["sales", "date", "region"]].copy()
    df_formatted.columns = ["Sales", "Date", "Region"]

    # 6. Append this cleaned chunk to our list
    cleaned_frames.append(df_formatted)

# 7. Combine all three cleaned DataFrames into one big DataFrame
combined_df = pd.concat(cleaned_frames, ignore_index=True)

# 8. Save the final result to a single CSV file
output_path = "pink_morsel_sales.csv"
combined_df.to_csv(output_path, index=False)
