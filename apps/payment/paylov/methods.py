from typing import Tuple


class PaylovMethods:
    """
    Constants class for Paylov transaction methods.

    This class defines the available transaction methods for interacting with the Paylov service.
    """

    CHECK_TRANSACTION: str = "transaction.check"
    PERFORM_TRANSACTION: str = "transaction.perform"

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str], Tuple[str, str]]:
        return (
            (cls.CHECK_TRANSACTION, cls.CHECK_TRANSACTION),
            (cls.PERFORM_TRANSACTION, cls.PERFORM_TRANSACTION)
        )
