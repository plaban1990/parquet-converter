import os
import pandas as pd

SOURCE_FOLDER = "target"  # Change if CSVs are in a different folder

# Ensure target directory exists
os.makedirs(SOURCE_FOLDER, exist_ok=True)

# Convert CSV to Parquet and remove CSV files
for file in os.listdir(SOURCE_FOLDER):
    if file.endswith(".csv"):
        csv_path = os.path.join(SOURCE_FOLDER, file)
        parquet_path = os.path.join(SOURCE_FOLDER, file.replace(".csv", ".parquet"))

        try:
            df = pd.read_csv(csv_path)
            df.to_parquet(parquet_path, engine='pyarrow')
            print(f"✅ Converted: {csv_path} -> {parquet_path}")
            
            # Remove CSV after successful conversion
            os.remove(csv_path)
            print(f"🗑️ Deleted: {csv_path}")
        except Exception as e:
            print(f"❌ Error processing {csv_path}: {e}")

print("🎉 All CSV files converted to Parquet and removed!")
