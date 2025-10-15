from typing import Tuple, Optional
# from payment.models import Providers


def get_credentials() -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Get Paylov API credentials.

    This function retrieves the Paylov API credentials (API key, username, password, subscription key)
    from the database.

    Returns:
        Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]: A tuple containing Paylov API credentials.
            - PAYLOV_API_KEY: The API key for Paylov.
            - PAYLOV_USERNAME: The username for Paylov.
            - PAYLOV_PASSWORD: The password for Paylov.
            - PAYLOV_SUBSCRIPTION_KEY: The subscription key for Paylov.
    """

    # PAYLOV = Providers.objects.filter(provider=Providers.ProviderChoices.PAYLOV, is_active=True)
    # PAYLOV_API_KEY = getattr(PAYLOV.filter(key="PAYLOV_API_KEY").last(), "value", None)
    # PAYLOV_USERNAME = getattr(PAYLOV.filter(key="PAYLOV_USERNAME").last(), "value", None)
    # PAYLOV_PASSWORD = getattr(PAYLOV.filter(key="PAYLOV_PASSWORD").last(), "value", None)
    # PAYLOV_SUBSCRIPTION_KEY = getattr(PAYLOV.filter(key="PAYLOV_SUBSCRIPTION_KEY").last(), "value", None)
    # PAYLOV_REDIRECT_URL = getattr(PAYLOV.filter(key="PAYLOV_REDIRECT_URL").last(), "value", None)

    # return {
    #     'PAYLOV_API_KEY': PAYLOV_API_KEY,
    #     'PAYLOV_USERNAME': PAYLOV_USERNAME,
    #     "PAYLOV_PASSWORD": PAYLOV_PASSWORD,
    #     "PAYLOV_SUBSCRIPTION_KEY": PAYLOV_SUBSCRIPTION_KEY,
    #     "PAYLOV_REDIRECT_URL": PAYLOV_REDIRECT_URL
    # }
