from django.core.management.base import BaseCommand, CommandError
from payment.models import Providers


class Command(BaseCommand):
    help = 'Add payments credentials to database'

    def handle(self, *args, **options):
        payment_credentials_dict = [
            # Paylov Credentials
            {
                "provider": Providers.ProviderChoices.PAYLOV,
                "key": "PAYLOV_API_KEY",
                "key_description": "Paylov API key"
            },
            {
                "provider": Providers.ProviderChoices.PAYLOV,
                "key": "PAYLOV_USERNAME",
                "key_description": "Paylov username"
            },
            {
                "provider": Providers.ProviderChoices.PAYLOV,
                "key": "PAYLOV_PASSWORD",
                "key_description": "Paylov password"
            },
            {
                "provider": Providers.ProviderChoices.PAYLOV,
                "key": "PAYLOV_SUBSCRIPTION_KEY",
                "key_description": "Paylov subscription key"
            },
            {
                "provider": Providers.ProviderChoices.PAYLOV,
                "key": "PAYLOV_REDIRECT_URL",
                "key_description": "Paylov redirect url for after payment"
            },
            # Payme Credentials
            {
                "provider": Providers.ProviderChoices.PAYME,
                "key": "PAYME_SECRET_KEY",
                "key_description": "Payme secret key"
            },
            {
                "provider": Providers.ProviderChoices.PAYME,
                "key": "PAYME_TEST_SECRET_KEY",
                "key_description": "Payme test secret key"
            },
            {
                "provider": Providers.ProviderChoices.PAYME,
                "key": "PAYME_FIELD_NAME_FOR_ID",
                "key_description": "Transaction id field name (Rekvizit)"
            },
            {
                "provider": Providers.ProviderChoices.PAYME,
                "key": "PAYME_KASSA_ID",
                "key_description": "Payme kassa ID"
            },
            {
                "provider": Providers.ProviderChoices.PAYME,
                "key": "PAYME_REDIRECT_URL",
                "key_description": "Payme redirect url for after payment"
            },
            # ClickUP Credentials
            {
                "provider": Providers.ProviderChoices.CLICK,
                "key": "CLICK_SECRET_KEY",
                "key_description": "ClickUP secret key"
            },
            {
                "provider": Providers.ProviderChoices.CLICK,
                "key": "CLICK_MERCHANT_ID",
                "key_description": "ClickUP merchant ID"
            },
            {
                "provider": Providers.ProviderChoices.CLICK,
                "key": "CLICK_MERCHANT_SERVICE_ID",
                "key_description": "ClickUP merchant service ID"
            },
            {
                "provider": Providers.ProviderChoices.CLICK,
                "key": "CLICK_REDIRECT_URL",
                "key_description": "ClickUP redirect url for after payment"
            },
            {
                "provider": Providers.ProviderChoices.CLICK,
                "key": "CLICK_MERCHANT_USER_ID",
                "key_description": "ClickUP merchant user id"
            }
        ]

        for credential in payment_credentials_dict:
            get, _ = Providers.objects.update_or_create(
                provider=credential["provider"],
                key=credential["key"],
                defaults={
                    "key_description": credential["key_description"]
                }
            )

            print(f"{get.key} is generated")


