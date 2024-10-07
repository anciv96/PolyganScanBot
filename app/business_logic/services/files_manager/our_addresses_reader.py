from typing import Any, Dict

from app import logger_setup
from app.business_logic.services.files_manager.file_utils import find_file_in_folder, get_data_frame
from app.config import ADDRESSES_FOLDER

logger = logger_setup.get_logger(__name__)


async def get_our_tokens() -> Dict[Any, Any]:
    """
    Retrieves tokens from the first found Excel or CSV file in the ADDRESSES_FOLDER.

    Returns:
        dict: A dictionary where the keys and values are the first and second columns of the file.

    Raises:
        ValueError: If the file cannot be found or there's an issue reading the file.
    """
    file_path = await find_file_in_folder(ADDRESSES_FOLDER, extensions=('.xlsx', '.csv'))

    if not file_path:
        return {}

    try:
        df = await get_data_frame(file_path)
        tokens = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        return tokens

    except FileNotFoundError:
        raise ValueError(f"File '{file_path}' not found.")
    except ValueError:
        raise ValueError("Error reading sheet from Excel file. Ensure that the sheet exists and the file is valid.")
    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        raise











