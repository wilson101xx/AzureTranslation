import json
import logging
from azure.core.exceptions import HttpResponseError
from src.clients.text_client import create_client

# Configure Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def get_language_info() -> dict:
    """Fetch language info from Azure Translator API and return as a dictionary."""
    logger.info("Initializing Azure Translator client...")
    text_translator = create_client()

    if not text_translator:
        logger.error("Failed to initialize Azure Translator client. Exiting function.")
        return {"error": "Translator client initialization failed."}

    try:
        logger.info("Fetching available languages from Azure Translator API...")
        response = text_translator.get_languages()
        response_dict = vars(response)  # ✅ Convert object to dictionary
        
        logger.info("Successfully retrieved language information.")
        return response_dict  # ✅ Return instead of saving to a file

    except HttpResponseError as e:
        logger.error(f"API request failed with error: {e}")
        return {"error": f"API request failed: {str(e)}"}

    except Exception as e:
        logger.exception(f"Unexpected error while fetching language information: {e}")
        return {"error": "An unexpected error occurred."}

if __name__ == "__main__":
    logger.info("Running language info retrieval script.")
    result = get_language_info()
    if "error" in result:
        logger.error(f"Language retrieval failed: {result['error']}")
    else:
        logger.info("Language retrieval successful.")

