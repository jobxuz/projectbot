CARDS = {
    "data": {
        "cardTypes": [
            {"id": "1", "processing": "UZCARD", "vendor": "UZCARD", "ranges": [{"start": "860000", "end": "860099"}]},
            {
                "id": "2",
                "processing": "UZCARD",
                "vendor": "UNIONPAY",
                "ranges": [
                    {"start": "626247", "end": "626249"},
                    {"start": "626253", "end": "626253"},
                    {"start": "626255", "end": "626257"},
                    {"start": "626263", "end": "626263"},
                    {"start": "626272", "end": "626273"},
                    {"start": "626282", "end": "626283"},
                    {"start": "626291", "end": "626292"},
                    {"start": "626296", "end": "626296"},
                    {"start": "626418", "end": "626418"},
                    {"start": "626425", "end": "626425"},
                ],
            },
            # {"id": "3", "processing": "UZCARD", "vendor": "MIR", "ranges": [{"start": "561468", "end": "561468"}]},
            {
                "id": "4",
                "processing": "UZCARD",
                "vendor": "MASTERCARD",
                "ranges": [{"start": "544081", "end": "544081"}],
            },
            {
                "id": "5",
                "processing": "HUMO",
                "vendor": "HUMO",
                "ranges": [
                    {"start": "986001", "end": "986004"},
                    {"start": "986006", "end": "986006"},
                    {"start": "986008", "end": "986010"},
                    {"start": "986012", "end": "986021"},
                    {"start": "986023", "end": "986035"},
                    {"start": "986060", "end": "986060"},
                ],
            },
            {
                "id": "6",
                "processing": "HUMO",
                "vendor": "VISA",
                "ranges": [
                    {"start": "400847", "end": "400847"},
                    {"start": "407342", "end": "407342"},
                    {"start": "418783", "end": "418783"},
                    {"start": "429434", "end": "429434"},
                ],
            },
            {"id": "7", "processing": "HUMO", "vendor": "MASTERCARD", "ranges": [{"start": "555536", "end": "555536"}]},
        ]
    }
}


def get_card_identifier(card_number):
    for card_type in CARDS["data"]["cardTypes"]:
        for system_card in card_type["ranges"]:
            if card_number == system_card["start"][:5] or card_number in system_card["end"][:5]:
                return {"source": card_type["processing"], "vendor": card_type["vendor"]}


# Card name constants
AMEX = "AMEX"
DISCOVER = "Discover"
MASTERCARD = "MasterCard"
VISA = "Visa"
UNKNOWN = "Unknown"

# Card number constants
AMEX_2 = ("34", "37")
MASTERCARD_2 = ("51", "52", "53", "54", "55")
DISCOVER_2 = ("65",)
DISCOVER_4 = ("6011",)
VISA_1 = "4"


def identify_card_type_four_digits(card_num):
    """
    Identifies the card type based on the card number.
    This information is provided through the first 4 digits of the card number.

    Input: Card number, int or string (4 digits)
    Output: Card type, string

    >>> identify_card_type_four_digits('3700')
    'AMEX'

    >>> identify_card_type_four_digits('6011')
    'Discover'

    >>> identify_card_type_four_digits('5424')
    'MasterCard'

    >>> identify_card_type_four_digits('4007')
    'Visa'

    >>> identify_card_type_four_digits('4008')
    'Unknown'
    """

    card_type = UNKNOWN
    card_num = str(card_num)[:4]

    # AMEX
    if len(card_num) == 4 and card_num[:2] in AMEX_2:
        card_type = AMEX

    # MasterCard, Visa, and Discover
    elif len(card_num) == 4:
        # MasterCard
        if card_num[:2] in MASTERCARD_2:
            card_type = MASTERCARD

        # Discover
        elif (card_num[:2] in DISCOVER_2) or (card_num[:4] in DISCOVER_4):
            card_type = DISCOVER

        # Visa
        elif card_num[:1].startswith(VISA_1):
            card_type = VISA

    return card_type
