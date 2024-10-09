import random

from apscheduler.triggers.interval import IntervalTrigger

from app import logger_setup
from app.dispatcher import scheduler
from app.telegram_bot.handlers.new_transactions_notifier.transaction_fetch_notifier import notify

logger = logger_setup.get_logger(__name__)


async def edit_scheduler_and_notify():
    await notify()
    delay = random.randint(20, 30)
    trigger = IntervalTrigger(seconds=delay)
    scheduler.modify_job(job_id='parse_job', trigger=trigger)
    logger.info(f'sleep for {delay}')


async def schedule_tasks():
    scheduler.add_job(edit_scheduler_and_notify, 'interval', seconds=20, replace_existing=False, max_instances=1,
                      coalesce=True, id='parse_job')

