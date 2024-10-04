from functools import wraps

from sqlalchemy.exc import StatementError


def session_start_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        self = args[0]
        try:
            async with self.session.begin():
                return await func(*args, **kwargs)
        except StatementError as e:
            await self.session.rollback()

    return wrapper
