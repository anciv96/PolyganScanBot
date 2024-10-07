import os
import pandas as pd
from typing import Optional


async def find_file_in_folder(folder_path: str, extensions: tuple) -> Optional[str]:
    """
    Finds the first file in the specified folder that matches one of the given extensions.

    Parameters:
        folder_path (str): Path to the folder to search in.
        extensions (tuple): File extensions to look for.

    Returns:
        str: The path to the found file, or None if no matching file is found.
    """
    for file in os.listdir(folder_path):
        if file.endswith(extensions):
            return os.path.join(folder_path, file)
    return None


async def get_data_frame(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV or Excel file into a Pandas DataFrame.

    Parameters:
        file_path (str): Path to the file to read.

    Returns:
        DataFrame: The loaded data as a Pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise FileNotFoundError(f"Unsupported file type: {file_path}")

    return df
