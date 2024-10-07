import os

from aiogram.types import Message

from app.config import ADDRESSES_FOLDER
from app.dispatcher import bot


async def handle_document(message):
    """
    Handles the processing of the uploaded document.

    Parameters:
        message (Message): The message object containing the document uploaded by the user.
    """
    file_name = message.document.file_name
    file_path = os.path.join(ADDRESSES_FOLDER, file_name)

    await _clear_folder(ADDRESSES_FOLDER)
    await _save_document(message, destination=file_path)


async def _save_document(message: Message, destination):
    """
    Downloads the uploaded document to a specified location.

    Parameters:
        message (Message): The message object containing the document to be downloaded.
        destination (str): The destination path where the file should be saved.
    """
    document = message.document
    await bot.download(document, destination=destination)


async def _clear_folder(folder_path):
    """
    Clears all files in the specified folder.

    Parameters:
        folder_path (str): The path to the folder to clear.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
