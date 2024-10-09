from aiogram.filters import Command
from aiogram.types import Message

from app.dispatcher import dp


@dp.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer('<b>Available commands:</b>\n\n'
                         '/update_wallets\n'
                         '/status')
