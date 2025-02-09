import pandas as pd
import sys

def csv_to_parquet(csv_file, parquet_file):
    """Convert CSV to Parquet"""
    df = pd.read_csv(csv_file)
    df.to_parquet(parquet_file, engine="pyarrow", index=False)
    print(f"Converted {csv_file} to {parquet_file}")

def parquet_to_csv(parquet_file, csv_file):
    """Convert Parquet to CSV"""
    df = pd.read_parquet(parquet_file, engine="pyarrow")
    df.to_csv(csv_file, index=False)
    print(f"Converted {parquet_file} to {csv_file}")

# Example Usage
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Convert CSV to Parquet: python script.py csv input.csv output.parquet")
        print("  Convert Parquet to CSV: python script.py parquet input.parquet output.csv")
        sys.exit(1)

    mode, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]

    if mode.lower() == "csv":
        csv_to_parquet(input_file, output_file)
    elif mode.lower() == "parquet":
        parquet_to_csv(input_file, output_file)
    else:
        print("Invalid mode! Use 'csv' for CSV to Parquet or 'parquet' for Parquet to CSV.")
