import csv
import random
import string
from datetime import datetime
import os
import pandas as pd

# Function to generate random values based on the type
def generate_value(data_type, input_element_name):
    if input_element_name in ['DOCUMENTACTIONCODE', 'actioncode']:
        return 'ADD'  # Override value if the input_element_name matches
    if data_type == 'String':
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Random string of 10 chars
    elif data_type == 'Date':
        return datetime.now().strftime("%Y-%m-%d")  # Current date in YYYY-MM-DD format
    elif data_type == 'integer':
        return random.randint(1, 1000)  # Random integer between 1 and 1000
    elif data_type == 'Double':
        return round(random.uniform(1, 1000), 2)  # Random float (double) rounded to 2 decimal places
    elif data_type == 'Timestamp':
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # Current UTC timestamp in YYYYMMDDTHHMMSSZ format
    elif data_type == 'Boolean':
        return random.choice([True, False])  # Random Boolean value
    else:
        return "N/A"  # In case of unknown type

# Define the input and output directories
input_directory = './entityFiles/'
output_directory = './target/'

# Function to read the input element and type from the CSV file
def read_input_elements_from_csv(csv_filename):
    input_elements = []
    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]  # Extract base name of the file (without extension)
    with open(csv_filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            input_element_name, data_type = row
            input_elements.append((input_element_name, data_type))
    return input_elements, base_filename

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):  # Process only CSV files
        input_csv_filename = os.path.join(input_directory, filename)

        # Read input elements and types from the CSV file
        input_elements, base_filename = read_input_elements_from_csv(input_csv_filename)

        # Generate the header and values
        header = [element[0] for element in input_elements]
        rows = []

        # Generate 10 rows of data
        for _ in range(10):
            row = [generate_value(data_type, input_element_name) for input_element_name, data_type in input_elements]
            rows.append(row)

        # Generate the current timestamp for the filename
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        # Generate a unique number for the filename (e.g., random or sequential)
        unique_number = random.randint(1000, 9999)

        # Create the CSV filename in the format 'inventoryTransactions_timestamp_number.csv'
        output_filename_csv = f"{base_filename}_{timestamp}_{unique_number}.csv"
        output_filename_parquet = f"{base_filename}_{timestamp}_{unique_number}.parquet"

        # Full path of the output files
        output_filepath_csv = os.path.join(output_directory, output_filename_csv)
        output_filepath_parquet = os.path.join(output_directory, output_filename_parquet)

        # Write the data to the output CSV file
        with open(output_filepath_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header
            writer.writerows(rows)  # Write the generated rows

        # Write the data to the output Parquet file using pandas
        df = pd.DataFrame(rows, columns=header)
        df.to_parquet(output_filepath_parquet, engine='pyarrow')

        print(f"CSV file created: {output_filepath_csv}")
        print(f"Parquet file created: {output_filepath_parquet}")
