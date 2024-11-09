
import requests
import logging

# Set up logger
logger = logging.getLogger(__name__)

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another.

    Args:
        amount (float): The amount of money to convert. Must be a positive number.
        from_currency (str): The 3-letter code of the source currency (e.g., 'USD', 'EUR').
        to_currency (str): The 3-letter code of the target currency (e.g., 'JPY', 'GBP').

    Returns:
        str: A string containing the converted amount or an error message.

    Example:
        >>> convert_currency(100, 'USD', 'EUR')
        '100 USD is equal to 84.23 EUR.'

    Raises:
        ValueError: If the input parameters are invalid.
        requests.RequestException: If there's an error fetching exchange rates.
    """
    logger.info(f"Converting {amount} from {from_currency} to {to_currency}")
    try:
        # Input validation
        if not isinstance(amount, (int, float)) or amount <= 0:
            return "Error: Amount must be a positive number."
        if not isinstance(from_currency, str) or len(from_currency) != 3:
            return "Error: From currency must be a 3-letter currency code."
        if not isinstance(to_currency, str) or len(to_currency) != 3:
            return "Error: To currency must be a 3-letter currency code."

        api_key = "98908dda318a32b7c9788e18"  # Replace with your actual API key
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        if to_currency not in data['rates']:
            return f"Error: Unable to convert to {to_currency}. Currency not supported."
        
        rate = data['rates'][to_currency]
        converted_amount = amount * rate
        
        result = f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}."
        logger.info(f"Conversion result: {result}")
        return result
    except Exception as e:
        error_message = f"Error in currency conversion: {str(e)}"
        logger.error(error_message)
        return error_message
    except Exception as e:        return f"Error: An unexpected error occurred. {str(e)}"