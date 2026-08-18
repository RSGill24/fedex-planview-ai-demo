# Azure Implementation Notes if Asked

The prototype is GCP-native, but the architectural pattern could be implemented on Azure if required.

| GCP demo component | Azure equivalent |
|---|---|
| Vertex AI / Gemini | Azure OpenAI / Azure AI Foundry |
| BigQuery | Databricks SQL, Synapse, or Fabric Warehouse |
| Cloud Storage | ADLS Gen2 |
| Knowledge Catalog / Dataplex | Microsoft Purview + Unity Catalog concepts |
| Cloud Run | Azure Container Apps / App Service / Functions |
| BigQuery row/column controls | Unity Catalog, Purview policies, Entra groups |

Recommendation: keep the demo GCP-native because FedEx future direction is GCP. Use Azure only as a response to implementation questions.
