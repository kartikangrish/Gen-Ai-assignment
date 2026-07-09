import csv
import os
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.transport import RequestsTransport
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchField, SearchFieldDataType, SearchIndex, SimpleField
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "house_rent_sample.csv"
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "house-rent-index")
SEARCH_VERIFY_SSL = os.getenv("AZURE_SEARCH_VERIFY_SSL", "true").lower() != "false"


def build_index() -> SearchIndex:
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="city", type=SearchFieldDataType.String, searchable=True, filterable=True),
        SimpleField(name="area_sqft", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(name="bhk", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(name="bathrooms", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SearchField(name="furnishing", type=SearchFieldDataType.String, searchable=True, filterable=True),
        SearchField(name="status", type=SearchFieldDataType.String, searchable=True, filterable=True),
        SearchField(name="tenant_preferred", type=SearchFieldDataType.String, searchable=True, filterable=True),
        SimpleField(name="rent", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
    ]
    return SearchIndex(name=INDEX_NAME, fields=fields)


def load_documents() -> list[dict]:
    with DATASET_PATH.open(newline="", encoding="utf-8") as dataset_file:
        reader = csv.DictReader(dataset_file)
        documents = []
        for row in reader:
            documents.append(
                {
                    "id": row["id"],
                    "city": row["city"],
                    "area_sqft": int(row["area_sqft"]),
                    "bhk": int(row["bhk"]),
                    "bathrooms": int(row["bathrooms"]),
                    "furnishing": row["furnishing"],
                    "status": row["status"],
                    "tenant_preferred": row["tenant_preferred"],
                    "rent": int(row["rent"]),
                }
            )
        return documents


def main():
    if not SEARCH_ENDPOINT or not SEARCH_KEY:
        raise RuntimeError("Set AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_KEY before creating the index.")

    credential = AzureKeyCredential(SEARCH_KEY)
    transport = RequestsTransport(connection_verify=SEARCH_VERIFY_SSL)
    index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=credential, transport=transport)
    index_client.create_or_update_index(build_index())

    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=credential,
        transport=RequestsTransport(connection_verify=SEARCH_VERIFY_SSL),
    )
    result = search_client.upload_documents(load_documents())
    uploaded = sum(1 for item in result if item.succeeded)
    print(f"Created index '{INDEX_NAME}' and uploaded {uploaded} documents.")


if __name__ == "__main__":
    main()