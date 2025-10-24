from django.urls import path, include




urlpatterns = [
    path("service/", include("apps.application.api_endpoint.AdditionalService.urls")),
    path("application/", include("apps.application.api_endpoint.Application.urls")),
    path("slider/", include("apps.application.api_endpoint.Slider.urls")),
    path("manufacturer/", include("apps.application.api_endpoint.Manufacturer.urls")),
    path("customer/", include("apps.application.api_endpoint.Customer.urls")),
    path("bot-user/", include("apps.application.api_endpoint.BotUser.urls")),
    path("package/", include("apps.application.api_endpoint.Package.urls")),
    path("offer/", include("apps.application.api_endpoint.Offer.urls")),
    path("segment/", include("apps.application.api_endpoint.Segment.urls")),
    path("contact-settings/", include("apps.application.api_endpoint.ContactSettings.urls")),
    path("paylov/", include("apps.payment.paylov.urls")),

]