import pandas as pd  


input_files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv",
]


cleaned_frames = []

for file_path in input_files:
    
    df = pd.read_csv(file_path)

    
    df["product"] = df["product"].str.lower()
    df_pink = df[df["product"].isin(["pink morsel"])].copy()

    
    df_pink["quantity"] = pd.to_numeric(df_pink["quantity"], errors="coerce")

    df_pink["price"] = (
        df_pink["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.strip()
    )
    df_pink["price"] = pd.to_numeric(df_pink["price"], errors="coerce")

    df_pink["sales"] = df_pink["quantity"] * df_pink["price"]

    
    df_formatted = df_pink[["sales", "date", "region"]].copy()
    df_formatted.columns = ["Sales", "Date", "Region"]

    
    cleaned_frames.append(df_formatted)


combined_df = pd.concat(cleaned_frames, ignore_index=True)


output_path = "pink_morsel_sales.csv"
combined_df.to_csv(output_path, index=False)
