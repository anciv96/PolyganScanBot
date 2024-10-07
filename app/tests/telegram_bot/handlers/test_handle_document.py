import os

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.config import ADDRESSES_FOLDER
from app.telegram_bot.handlers.update_wallets_command import handle_document


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.update_wallets_command.handle_document._save_document", new_callable=AsyncMock)
@patch("app.telegram_bot.handlers.update_wallets_command.handle_document._clear_folder", new_callable=AsyncMock)
async def test_handle_document(mock_clear_folder, mock_save_document):
    mock_message = MagicMock()
    mock_message.document.file_name = "test_document.txt"

    await handle_document.handle_document(mock_message)

    mock_clear_folder.assert_awaited_once_with(ADDRESSES_FOLDER)

    expected_file_path = os.path.join(ADDRESSES_FOLDER, 'test_document.txt')
    mock_save_document.assert_awaited_once_with(mock_message, destination=expected_file_path)
