import os
import requests
import json
import logging
from src.clients.doc_intel_client import document_client
from src.libs.format_extension import get_format_from_extension
from src.modules.get_language_info import get_language_info
from azure.ai.translation.document.models import DocumentTranslateContent
from src.config.local_env import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def get_language_code(language_name) -> str:
    """
    Converts a language name to the Azure translation language code.
    Example: 'English' -> 'en'
    """
    try:
        language_data = get_language_info()
        translation = language_data["_data"].get("translation", {})
        for code, details in translation.items():
            if details.get("name", "").lower() == language_name.lower():
                logger.info(f"Found language code '{code}' for language '{language_name}'.")
                return code

        logger.warning(f"Language '{language_name}' not found in the translation data.")
        return None

    except Exception as e:
        logger.exception(f"Error retrieving language code for '{language_name}': {e}")
        return None

def document_translation(source_document, source_language_code, target_language_code):
    """
    Sends the document to the Azure Document Translation API,
    saves the translated file locally, and returns its file path.
    """
    try:
        if not all([source_document, source_language_code, target_language_code]):
            logger.error("Missing required parameters for document translation.")
            return None

        file_name = os.path.splitext(os.path.basename(source_document))[0]
        file_extension = os.path.splitext(source_document)[1]
        output_file_name = f"{file_name}_{target_language_code}{file_extension}"
        translated_dir = "translated_files"
        os.makedirs(translated_dir, exist_ok=True)
        output_file_path = os.path.join(translated_dir, output_file_name)

        fileformat = get_format_from_extension(file_extension)
        logger.info(f"Translating document '{source_document}' to '{target_language_code}' format '{fileformat}'.")

        params = {
            "sourceLanguage": source_language_code,
            "targetLanguage": target_language_code,
            "api-version": "2023-11-01-preview"
        }

        headers = {
            "Ocp-Apim-Subscription-Key": settings.AZURE_AI_KEY,
            "Ocp-Apim-Subscription-Region": "southcentralus"
        }

        url = settings.AZURE_AI_DOCUMENT_TRANSLATION + "translator/document:translate"

        with open(source_document, "rb") as document:
            data = {
                "document": (os.path.basename(source_document), document, fileformat)
            }
            response = requests.post(url, headers=headers, files=data, params=params)

        if response.status_code != 200:
            try:
                error_data = response.json()
            except json.JSONDecodeError:
                error_data = response.text
            logger.error(f"Translation failed (status code {response.status_code}): {error_data}")
            return None

        if "application/json" in response.headers.get("Content-Type", ""):
            error_data = response.json()
            logger.error(f"Translation error: {error_data}")
            return None

        with open(output_file_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Translated document saved at: {output_file_path}")
        return output_file_path

    except Exception as e:
        logger.exception(f"Error in document translation: {e}")
        return None

def main(document, source_language, target_languages):
    logger.info(f"Starting translation for document '{document}' from '{source_language}' to {target_languages}.")
    source_language_code = get_language_code(source_language)
    if not source_language_code:
        logger.error(f"Failed to get source language code for '{source_language}'. Skipping translation.")
        return

    for target_language in target_languages:
        target_language_code = get_language_code(target_language)
        if not target_language_code:
            logger.error(f"Skipping translation for '{target_language}' as language code could not be determined.")
            continue
        
        result = document_translation(document, source_language_code, target_language_code)
        if result:
            logger.info(f"Translation completed successfully: {result}")
        else:
            logger.error(f"Translation failed for {target_language}.")

if __name__ == "__main__":
    items = os.listdir("test_content")
    for i in items:
        source_document = os.path.join("test_content", i)
        source_language = "English"
        target_languages = ["Japanese"]
        main(source_document, source_language, target_languages)
