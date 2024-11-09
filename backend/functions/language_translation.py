
# from googletrans import Translator, LANGUAGES
import logging

# Set up logger
logger = logging.getLogger(__name__)

def translate_text(text: str, target_language: str) -> str:
    """
    Translate text to a target language.

    Args:
        text (str): The text to translate. Must be a non-empty string.
        target_language (str): The 2-letter code of the target language (e.g., 'es' for Spanish, 'fr' for French).

    Returns:
        str: A string containing the translated text or an error message.

    Example:
        >>> translate_text("Hello, world!", "es")
        'Translated text: ¡Hola, mundo!'

    Raises:
        ValueError: If the input parameters are invalid or the target language is not supported.
    """
    logger.info(f"Translating text to {target_language}")
    try:
        # Input validation
        # if not isinstance(text, str) or not text.strip():
        #     return "Error: Text to translate must be a non-empty string."
        # if not isinstance(target_language, str) or len(target_language) != 2:
        #     return "Error: Target language must be a 2-letter language code."
        # if target_language not in LANGUAGES:
        #     return f"Error: Invalid target language '{target_language}'. Please use a valid language code."

        # translator = Translator()
        # translation = translator.translate(text, dest=target_language)
        # result = f"Translated text: {translation.text}"
        # logger.info(f"Translation result: {result}")
        return result
    except Exception as e:
        error_message = f"Error in translation: {str(e)}"
        logger.error(error_message)
        return error_message    
    except Exception as e:        
        return f"Error: Translation failed. {str(e)}"