import pandas as pd
import sys

def csv_to_parquet(csv_file, parquet_file):
    df = pd.read_csv(csv_file)
    df.to_parquet(parquet_file, engine="pyarrow", index=False)
    print(f"Converted {csv_file} to {parquet_file}")

def parquet_to_csv(parquet_file, csv_file):
    df = pd.read_parquet(parquet_file, engine="pyarrow")
    df.to_csv(csv_file, index=False)
    print(f"Converted {parquet_file} to {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if input_file.endswith(".csv"):
        csv_to_parquet(input_file, output_file)
    elif input_file.endswith(".parquet"):
        parquet_to_csv(input_file, output_file)
    else:
        print("Unsupported file format!")
