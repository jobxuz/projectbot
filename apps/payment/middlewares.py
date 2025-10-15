# # middleware.py
# import json
# from apps.payment.models import Providers


# class LoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.provider_urls = {
#             "/api/payment/callbacks/payme/": Providers.ProviderChoices.PAYME,
#             "/api/payment/callbacks/paylov/": Providers.ProviderChoices.PAYLOV,
#             "/api/payment/callbacks/click/prepare/": Providers.ProviderChoices.CLICK,
#             "/api/payment/callbacks/click/complete/": Providers.ProviderChoices.CLICK,
#         }
#         self.click_methods = {
#             "/payment/callbacks/click/prepare/": "prepare",
#             "/payment/callbacks/click/complete/": "complete",
#         }

#     def __call__(self, request):
#         # Process request
#         self.process_request(request)

#         # Get response
#         response = self.get_response(request)

#         return response

#     def process_request(self, request):
#         if request.path in self.provider_urls.keys():
#             body = request.body.decode('utf-8')
#             try:
#                 method = json.loads(body).get("method", None) if body else None

#                 if str(request.path).startswith("/payments/callbacks/click/"):
#                     method = self.click_methods[request.path]
#             except:
#                 method = "prepare" if str(request.path).startswith("/payments/callbacks/click/prepare/") else "complete"

#             if not method:
#                 method = "test"