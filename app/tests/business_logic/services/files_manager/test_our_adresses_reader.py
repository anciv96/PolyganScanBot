import asyncio
import os
import pytest
import pandas as pd
from unittest.mock import patch, AsyncMock

from app.business_logic.services.files_manager import our_addresses_reader
from app.business_logic.services.files_manager.file_utils import find_file_in_folder
from app.business_logic.services.files_manager.file_utils import get_data_frame
from app.config import ADDRESSES_FOLDER


@pytest.mark.anyio
@patch("app.business_logic.services.files_manager.file_utils.find_file_in_folder", new_callable=AsyncMock)
@patch("app.business_logic.services.files_manager.file_utils.get_data_frame", new_callable=AsyncMock)
async def test_get_our_tokens_csv(mock_find_file_in_folder, mock_get_data_frame):
    mock_find_file_in_folder.return_value = 'test_tokens.csv'

    mock_data = pd.DataFrame({
        'Token': ['token1', 'token2'],
        'Value': ['value1', 'value2']
    })
    mock_get_data_frame.return_value = mock_data

    result = await our_addresses_reader.get_our_tokens()

    assert mock_find_file_in_folder.called
    expected_result = {'token1': 'value1', 'token2': 'value2'}
    assert result == expected_result


@pytest.mark.anyio
@patch("app.business_logic.services.files_manager.file_utils.find_file_in_folder", new_callable=AsyncMock)
@patch("app.business_logic.services.files_manager.file_utils.get_data_frame", new_callable=AsyncMock)
async def test_get_our_tokens_excel(mock_find_file_in_folder, mock_get_data_frame):
    mock_find_file_in_folder.return_value = 'test_tokens.csv'

    mock_data = pd.DataFrame({
        'Token': ['token3', 'token4'],
        'Value': ['value3', 'value4']
    })
    mock_get_data_frame.return_value = mock_data

    result = await our_addresses_reader.get_our_tokens()

    assert mock_find_file_in_folder.called
    expected_result = {'token3': 'value3', 'token4': 'value4'}
    assert result == expected_result


