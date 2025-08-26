from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


UNFOLD = {
    "SITE_TITLE": "Admin Panel",
    "SITE_HEADER": "Admin Panel",
    # "SITE_URL": "https://marjon.uz/",
    'ENABLE_IMPORT_EXPORT': True,
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("assets/img/admin-logo.svg"),  # dark mode
    # },
    # # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("assets/img/welcome-logo.svg"),  # light mode
    #     "dark": lambda request: static("assets/img/admin-logo.svg"),  # dark mode
    # },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    # "ENVIRONMENT": "apps.common.views.environment_callback",
    # "DASHBOARD_CALLBACK": "apps.user.dashboard.dashboard_callback",
    # "LOGIN": {
    #     "image": lambda request: static("assets/img/admin-welcome-image.svg"),
    # },
    "STYLES": [
        lambda request: static("assets/css/main.css"),
    ],
    "SCRIPTS": [
        lambda request: static("assets/js/admin.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "uz": "🇺🇿",
    #             "ru": "🇷🇺",
    #             "en": "🇬🇧",
    #         },
    #     },
    # },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            # Users
            {
                "title": _("Users"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:user_user_changelist"),
                    },
                ],
            },
            # applications
            {
                "title": _("Applications"),
                "separator": True,
                "items": [
                    {
                        "title": _("Ishlab chiqaruvchi"),
                        "icon": "factory",
                        "link": reverse_lazy("admin:application_manufacturer_changelist"),
                    },
                    {
                        "title": _("Buyurtmachi"),
                        "icon": "people",
                        "link": reverse_lazy("admin:application_customer_changelist"),
                    },
                ]
            },
            # ApplicationAdditionalService
            {
                "title": _("Application Additional Service"),
                "separator": True,
                "items": [
                    {
                        "title": _("Qo‘shimcha xizmat arizasi"),
                        "icon": "package",
                        "link": reverse_lazy("admin:application_applicationadditionalservice_changelist"),
                    },
                ],
            },
            # Services
            {
                "title": _("Additional Services"),
                "separator": True,
                "items": [
                    {
                        "title": _("Qo'shimcha xizmat"),
                        "icon": "package",
                        "link": reverse_lazy("admin:application_additionalservice_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "app_label.model_name_in_lowercase",
            ],
            "items": [
                {
                    "title": _("Your custom title"),
                    "link": reverse_lazy("admin:user_user_changelist"),
                    # "permission": "sample_app.permission_callback",
                },
            ],
        },
    ],
}


def badge_callback(request):
    return 3


def permission_callback(request):
    return request.user.has_perm("sample_app.change_model")
