import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    """Singleton class to store configuration values for Snowflake and Azure."""
    
    # Snowflake Configuration
    AZURE_AI_TRANSLATION_ENDPOINT = os.getenv("AZURE_AI_TRANSLATION_ENDPOINT")
    AZURE_AI_TRANSLATION_ENDPOINTDOCUMENT = os.getenv("AZURE_AI_TRANSLATION_ENDPOINTDOCUMENT")
    AZURE_AI_TRANSLATION_KEY = os.getenv("AZURE_AI_TRANSLATION_KEY")
    AZURE_AI_TRANSLATION_REGION = os.getenv("AZURE_AI_TRANSLATION_REGION")
    AZURE_AI_DOCUMENT_TRANSLATION = os.getenv("AZURE_AI_DOCUMENT_TRANSLATION")
    AZURE_AI_KEY = os.getenv("AZURE_AI_KEY")