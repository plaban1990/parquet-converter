import os
import pandas as pd

SOURCE_FOLDER = "target"  # Change to your CSV folder
OUTPUT_FOLDER = "target"  # Output will be saved in the same folder

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Convert all CSV files in the folder
for file in os.listdir(SOURCE_FOLDER):
    if file.endswith(".csv"):
        csv_path = os.path.join(SOURCE_FOLDER, file)
        parquet_path = os.path.join(OUTPUT_FOLDER, file.replace(".csv", ".parquet"))

        try:
            df = pd.read_csv(csv_path)
            df.to_parquet(parquet_path, engine='pyarrow')
            print(f"✅ Converted: {csv_path} -> {parquet_path}")
        except Exception as e:
            print(f"❌ Error processing {csv_path}: {e}")

print("🎉 All CSV files converted to Parquet!")
