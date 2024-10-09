from aiogram.filters import Command
from aiogram.types import Message

from app.dispatcher import dp


@dp.message(Command('status'))
async def command_status(message: Message) -> None:
    await message.answer('Working 🟢')
