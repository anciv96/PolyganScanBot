from functools import wraps

from sqlalchemy.exc import StatementError


def session_start_decorator(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            async with self.session.begin():
                return await func(self, *args, **kwargs)
        except StatementError as e:
            await self.session.rollback()

    return wrapper
