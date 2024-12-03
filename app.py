from flask import Flask, render_template_string
from azure.storage.blob import BlobServiceClient
import pandas as pd
import os

app = Flask(__name__)

# Connection details
CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "bankcustomerdata"

def read_csv_from_blob(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blob_client = container_client.get_blob_client(blob_name)
    downloaded_blob = blob_client.download_blob()
    csv_data = downloaded_blob.content_as_text()
    df = pd.read_csv(pd.compat.StringIO(csv_data))
    return df

@app.route('/')
def display_csv():
    # Fetch CSV data
    df = read_csv_from_blob('BankChurners.csv')
    
    # Convert DataFrame to HTML
    table_html = df.to_html(classes="table table-bordered", index=False)
    
    # Render HTML with the table
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <title>CSV Data</title>
    </head>
    <body>
        <div class="container mt-4">
            <h1>CSV Data</h1>
            {{ table_html|safe }}
        </div>
    </body>
    </html>
    """, table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)