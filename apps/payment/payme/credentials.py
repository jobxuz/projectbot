from typing import Tuple, Optional
from payment.models import Providers


def get_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Get Paylov API credentials.

    This function retrieves the Paylov API credentials (API key, username, password, subscription key)
    from the database.

    Returns:
        Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]: A tuple containing Paylov API credentials.
            - PAYME_SECRET_KEY: The API key for Payme.
            - PAYME_TEST_SECRET_KEY: The test API key for Payme.
    """

    PAYME = Providers.objects.filter(provider=Providers.ProviderChoices.PAYME, is_active=True)
    PAYME_SECRET_KEY = getattr(PAYME.filter(key="PAYME_SECRET_KEY").last(), "value", None)
    PAYME_KASSA_ID = getattr(PAYME.filter(key="PAYME_KASSA_ID").last(), "value", None)
    PAYME_TEST_SECRET_KEY = getattr(PAYME.filter(key="PAYME_TEST_SECRET_KEY").last(), "value", None)
    PAYME_FIELD_NAME_FOR_ID = getattr(PAYME.filter(key="PAYME_FIELD_NAME_FOR_ID").last(), "value", None)
    PAYME_REDIRECT_URL = getattr(PAYME.filter(key="PAYME_REDIRECT_URL").last(), "value", None)

    return {
        "PAYME_SECRET_KEY": PAYME_SECRET_KEY,
        "PAYME_TEST_SECRET_KEY": PAYME_TEST_SECRET_KEY,
        "PAYME_FIELD_NAME_FOR_ID": PAYME_FIELD_NAME_FOR_ID,
        "PAYME_KASSA_ID": PAYME_KASSA_ID,
        "PAYME_REDIRECT_URL": PAYME_REDIRECT_URL
    }
