"""Database utilities module."""

from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

from sqlalchemy.exc import SQLAlchemyError


T = TypeVar("T")
AsyncCallable = Callable[..., Coroutine[Any, Any, T]]


def handle_crud_operation(func: AsyncCallable[T]) -> AsyncCallable[T]:
    """Wrap a CRUD operation to catch errors and rollback the transaction.

    This allows to handle operations errors for all CRUD operations without
    having to add a try-except block to each operation.

    Args:
        func: The CRUD operation to wrap.

    Returns:
        The wrapped CRUD operation.
    """

    @wraps(func)
    async def wrapper(self, *args: Any, **kwargs: Any) -> T:
        try:
            return await func(self, *args, **kwargs)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    return wrapper
