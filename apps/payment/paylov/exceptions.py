from typing import Any


class PaylovBadResponseException(Exception):
    """
    Exception raised for a bad response from the Paylov service.

    Attributes:
        response: The response received from the Paylov service.
        kwargs: Additional keyword arguments.
    """
    def __init__(self, response: Any, **kwargs: Any) -> None:
        """
        Initialize the exception with the response and additional arguments.

        Args:
            response (Any): The response received from the Paylov service.
            **kwargs (Any): Additional keyword arguments.
        """
        self.response = response
        self.kwargs = kwargs