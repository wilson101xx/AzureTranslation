# 🌐 Document Translator with Azure AI

This project is a Python-based FastAPI application that allows users to upload documents and translate them into one or more target languages using Azure AI Translator.


## 🚀 Features
- 🌍 Translate documents into multiple languages using Azure AI

- 📤 Upload a single file via FastAPI endpoints

- 🖥️ Support for local file translation or API-based translation

- 🧠 Language detection and validation via Azure

- 🗂️ Automatically returns translated files or zipped package for multiple outputs

- 🪶 Built using Python, FastAPI, and Azure Translator SDKs




``` 
src/
├── api/
│   ├── main.py                # FastAPI app entrypoint
│   ├── routes/
│   │   ├── translation.py     # Upload and translate files
│   │   └── languages.py       # Fetch available languages
├── clients/
│   ├── doc_intel_client.py    # Azure document translation client
│   └── text_client.py         # Azure text translation client
├── config/
│   └── local_env.py           # Environment variable loader
├── libs/
│   └── format_extensions.py   # Maps file extensions to MIME types
├── modules/
│   ├── get_language_info.py   # Azure language info fetcher
│   └── translate_documents.py # Core document translation logic
```

## How to run

1. Install dependencies
``` 
pip install -r requirements.txt
 ```

 2. Set environment variables (via .env or system):

    - AZURE_AI_TRANSLATION_ENDPOINT

    - AZURE_AI_TRANSLATION_KEY

    - AZURE_AI_TRANSLATION_REGION

    - AZURE_AI_DOCUMENT_TRANSLATION

    - AZURE_AI_KEY

3. Run the app
``` 
uvicorn src.api.main:app --reload
```



## API Endpoints

```POST /translation/upload```: Upload and translate a file.

```GET /languages/get_languages```: Get available translation languages.



# TODO:

- Create the Modules needed for Azure AI translation - Done
- Create FastAPI endpoints for it - Done
- Create a streamlit app to run the application
- Create a notebook working through it
- Give option for using App Config


