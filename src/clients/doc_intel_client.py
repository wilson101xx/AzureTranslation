import logging
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import SingleDocumentTranslationClient
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from src.config.local_env import Settings
import sys


settings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def document_client():
    """Creates and returns a SingleDocumentTranslationClient with logging."""
    try:
        endpoint = settings.AZURE_AI_TRANSLATION_ENDPOINT
        key = settings.AZURE_AI_TRANSLATION_KEY
        region = settings.AZURE_AI_TRANSLATION_REGION

        logger.info("Initializing SingleDocumentTranslationClient...")

        if not endpoint or not key:
            logger.error("Missing required credentials: Ensure AZURE_AI_TRANSLATION_ENDPOINT and AZURE_AI_TRANSLATION_KEY are set.")
            return None

        client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))

        logger.info("SingleDocumentTranslationClient initialized successfully.")
        return client

    except Exception as e:
        logger.exception("Error initializing SingleDocumentTranslationClient: %s", e)
        return None

if __name__ == "__main__":
    client = document_client()
    if client:
        logger.info("Client is ready for use.")
    else:
        logger.error("Failed to initialize the translation client.")
