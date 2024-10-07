from app.dispatcher import scheduler
from app.telegram_bot.handlers.new_transactions_notifier.transaction_fetch_notifier import notify


async def schedule_tasks():
    scheduler.add_job(notify, 'interval', seconds=20, replace_existing=False, max_instances=1,
                      coalesce=True)

