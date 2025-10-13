from typing import Any


class PaymentFailureException(Exception):
    """
    Exception raised if no cards.

    Attributes:
        kwargs: Additional keyword arguments.
    """

    def __init__(self, detail: Any = None, code: Any = None) -> None:
        """
        Initialize the exception with the response and additional arguments.

        Args:
            **kwargs (Any): Additional keyword arguments.
        """

        self.detail = detail
        self.code = code
