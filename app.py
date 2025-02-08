from flask import Flask, request, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    converted_file_path = convert_file(file_path)
    converted_filename = os.path.basename(converted_file_path)

    return jsonify({
        "filename": converted_filename,
        "download_url": f"/download/{converted_filename}"
    })


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(CONVERTED_FOLDER, filename), as_attachment=True)


def convert_file(file_path):
    filename, ext = os.path.splitext(file_path)
    if ext == ".csv":
        df = pd.read_csv(file_path)
        converted_file = f"{filename}.parquet"
        df.to_parquet(converted_file, index=False)
    elif ext == ".parquet":
        df = pd.read_parquet(file_path)
        converted_file = f"{filename}.csv"
        df.to_csv(converted_file, index=False)
    else:
        raise ValueError("Unsupported file format")

    new_path = os.path.join(CONVERTED_FOLDER, os.path.basename(converted_file))
    os.rename(converted_file, new_path)
    return new_path


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
