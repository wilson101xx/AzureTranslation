# AzureTranslation
This is a repo that shows how too use the AI Translation tool



# TODO:

- Create the Modules needed for Azure AI translation
- Create FastAPI endpoints for it
- Create a streamlit app to run the application
- Create a notebook working through it
- Give option for using App Config


azure-ai-translation-tool/
│
├── src/
│   ├── client/
│   │   └── translation_client.py
│   │
│   ├── config/
│   │   └── keys_loader.py
│   │
│   ├── modules/
│   │   └── document_translation.py
│   │
│   ├── api/
│   │   └── main.py
│
├── streamlit_app/
│   ├── app.py
│   └── components/
│
├── notebooks/
│   └── translation_demo.ipynb
│
├── tests/
│   ├── test_client.py
│   ├── test_keys_loader.py
│   └── test_document_translation.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── pyproject.toml
