from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import logger_setup
from app.dispatcher import dp
from app.telegram_bot.exceptions import WrongFileTypeError
from app.telegram_bot.handlers.new_transactions_notifier.transaction_fetch_notifier import notify
from app.telegram_bot.handlers.update_wallets_command.handle_document import handle_document
from app.telegram_bot.states.update_wallets import UpdateWallets


logger = logger_setup.get_logger(__name__)


@dp.message(Command('update_wallets'))
async def command_update_wallets(message: Message, state: FSMContext) -> None:
    """
    Handles the `/update_wallets` command to start the process of updating wallets.

    Parameters:
        message (Message): The message object that contains details about the command.
        state (FSMContext): The current state of the user in the finite state machine.
    """
    await message.answer('Send csv or xlsx file.')
    await state.set_state(UpdateWallets.get_file)


@dp.message(UpdateWallets.get_file)
async def command_get_wallets(message: Message, state: FSMContext) -> None:
    """
    Handles receiving the file from the user after the `/update_wallets` command.

    Parameters:
        message (Message): The message object containing the user's file or other input.
        state (FSMContext): The current state of the user in the finite state machine.
    """
    file_type = message.content_type
    if file_type == ContentType.DOCUMENT:
        try:
            await handle_document(message)
            await message.answer('Value retained 🟢')
            logger.info('New document saved')
            await state.clear()
        except WrongFileTypeError as error:
            logger.info(error)
            await message.answer('File must be excel or csv file. Try again: ')
            await state.set_state(UpdateWallets.get_file)
        except Exception as error:
            logger.error(error)
            await state.clear()
    else:
        await message.answer('❌ Action cancelled')
        await state.clear()

