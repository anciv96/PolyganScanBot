import asyncio

from app import logger_setup
from app.business_logic.models.database import engine, Base
from app.business_logic.scheduler import schedule_tasks
from app.dispatcher import bot, scheduler

from app.telegram_bot.handlers.update_wallets_command.update_wallets_handler import dp


logger = logger_setup.get_logger(__name__)


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def schedule_tasks_wrapper():
    try:
        logger.info('Starting schedule task')
        await schedule_tasks()
        scheduler.start()

    except Exception as error:
        logger.critical(f"Ошибка при запуске расписания задач: {error}")


async def main():
    await init_db()
    await schedule_tasks_wrapper()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

