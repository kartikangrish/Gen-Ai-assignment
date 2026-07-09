import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "house_rent_sample.csv"
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "house-rent-data")
BLOB_NAME = os.getenv("AZURE_STORAGE_BLOB_NAME", DATASET_PATH.name)


def main():
    if not CONNECTION_STRING:
        raise RuntimeError("Set AZURE_STORAGE_CONNECTION_STRING before uploading the dataset.")

    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    if not container_client.exists():
        container_client.create_container()

    with DATASET_PATH.open("rb") as dataset_file:
        container_client.upload_blob(
            name=BLOB_NAME,
            data=dataset_file,
            overwrite=True,
            content_settings=ContentSettings(content_type="text/csv"),
        )

    print(f"Uploaded {DATASET_PATH.name} to container '{CONTAINER_NAME}' as '{BLOB_NAME}'.")


if __name__ == "__main__":
    main()