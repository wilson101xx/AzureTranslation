import logging
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from src.config.local_env import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def create_client():
    """Creates and returns a TextTranslationClient with logging."""
    try:
        # Store environment variables into local variables
        endpoint = settings.AZURE_AI_TRANSLATION_ENDPOINT
        key = settings.AZURE_AI_TRANSLATION_KEY
        region = settings.AZURE_AI_TRANSLATION_REGION

        logger.info("Initializing TextTranslationClient...")

        # Check if required credentials are available
        if not endpoint or not key or not region:
            logger.error("Missing required credentials: Ensure AZURE_AI_TRANSLATION_ENDPOINT, AZURE_AI_TRANSLATION_KEY, and AZURE_AI_TRANSLATION_REGION are set.")
            return None

        # Create Azure Translator client
        credential = TranslatorCredential(key, region)
        text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

        logger.info("TextTranslationClient initialized successfully.")
        return text_translator

    except Exception as e:
        logger.exception("Error initializing TextTranslationClient: %s", e)
        return None

if __name__ == "__main__":
    client = create_client()
    if client:
        logger.info("Azure Translator client created successfully and ready for use.")
    else:
        logger.error("Failed to initialize the Azure Translator client.")
