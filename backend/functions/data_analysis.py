
import pandas as pd
import json
import logging

# Set up logger
logger = logging.getLogger(__name__)

def analyze_data(data: str, analysis_type: str) -> str:
    logger.info(f"Analyzing data with analysis type: {analysis_type}")
    """
    Perform data analysis on provided JSON data.

    Args:
        data (str): A JSON string representing the data to analyze. Must be valid JSON format.
        analysis_type (str): The type of analysis to perform. Must be either 'summary' or 'correlation'.

    Returns:
        str: A string containing the analysis results or an error message.

    Example:
        >>> sample_data = '{"col1": [1, 2, 3], "col2": [4, 5, 6]}'
        >>> analyze_data(sample_data, "summary")
        'Data summary: {"col1":{"count":3.0,"mean":2.0,"std":1.0,"min":1.0,"25%":1.5,"50%":2.0,"75%":2.5,"max":3.0},"col2":{"count":3.0,"mean":5.0,"std":1.0,"min":4.0,"25%":4.5,"50%":5.0,"75%":5.5,"max":6.0}}'

    Raises:
        ValueError: If the input parameters are invalid or the JSON data is malformed.
        pandas.errors.EmptyDataError: If the provided data is empty.
    """
    try:
        # Input validation
        if not isinstance(data, str):
            return "Error: Data must be a JSON string."
        if not isinstance(analysis_type, str):
            return "Error: Analysis type must be a string."
        if analysis_type not in ["summary", "correlation"]:
            return "Error: Analysis type must be either 'summary' or 'correlation'."

        # Validate JSON data
        json.loads(data)

        df = pd.read_json(data)
        
        if analysis_type == "summary":
            result = df.describe().to_json()
            logger.info(f"Analysis result: {result}")
            return f"Data summary: {result}"
        elif analysis_type == "correlation":
            result = df.corr().to_json()
            logger.info(f"Analysis result: {result}")
            return f"Correlation matrix: {result}"
    except Exception as e:
        logger.error(f"Error during data analysis: {str(e)}")
        return f"Error: Failed to analyze data. {str(e)}"    
    except Exception as e:        
        return f"Error: Failed to analyze data. {str(e)}"