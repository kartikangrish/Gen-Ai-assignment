# Day 2 Azure Agents App

This Flask app covers all three Day 2 assignments:

1. Chat App - uses your GPT-5 deployment in Azure OpenAI.
2. Policy Helper Agent - answers IT, password, acceptable use, and data protection policy questions.
3. House Rent Prediction Agent - searches a house rent dataset through Azure AI Search and uses GPT-5 to generate a grounded response.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env` with your Azure OpenAI and Azure AI Search values.

Run locally:

```powershell
python app.py
```

Open `http://localhost:8000`.

## Azure resources needed

- Azure OpenAI or Azure AI Foundry resource with a GPT-5 model deployment. The app supports a Foundry Responses API endpoint such as `/openai/v1/responses`.
- Storage account with a blob container for the house rent dataset.
- Azure AI Search service with an index created from the blob dataset.
- Azure App Service or Azure Container Apps to host this Flask app.

You can start with `data/house_rent_sample.csv`, upload it to blob storage, and import it into Azure AI Search. The search index should include searchable fields such as `city`, `area_sqft`, `bhk`, `bathrooms`, `furnishing`, `status`, `tenant_preferred`, and `rent`.

Helper scripts are included:

```powershell
python scripts/upload_house_rent_dataset.py
python scripts/create_house_rent_search_index.py
```

The first script uploads the sample CSV to your blob container. The second script creates the Azure AI Search index and uploads the CSV rows as searchable documents.

## Azure App Service deployment

Set these application settings in Azure App Service:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_API_VERSION
AZURE_OPENAI_DEPLOYMENT
AZURE_SEARCH_ENDPOINT
AZURE_SEARCH_KEY
AZURE_SEARCH_INDEX_NAME
AZURE_STORAGE_CONNECTION_STRING
AZURE_STORAGE_CONTAINER_NAME
AZURE_STORAGE_BLOB_NAME
```

For Linux App Service, set the startup command to:

```text
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```