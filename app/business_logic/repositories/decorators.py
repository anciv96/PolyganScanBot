from functools import wraps

from sqlalchemy.exc import StatementError

from app import logger_setup

logger = logger_setup.get_logger(__name__)


def session_start_decorator(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            async with self.session.begin():
                return await func(self, *args, **kwargs)
        except StatementError as e:
            logger.warning(e)
            await self.session.rollback()
        except Exception as error:
            logger.warning(error)
        finally:
            await self.session.close()

    return wrapper
