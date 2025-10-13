from book.models import Book
from study.models import Course, Discount


def calculate_amount_with_discount_promocode(discount, promocode, amount, user):
    if discount:
        discount_price = int((amount / 100) * discount.percentage)
        amount -= discount_price

    if promocode and user not in promocode.users_who_used.all():
        amount -= promocode.amount
        promocode.users_who_used.add(user)

    return amount


def get_discount_for_payment(book: Book, course: Course, today) -> object:
    filters = {
        "start_date__lte": today,
        "end_date__gte": today
    }
    if course:
        filters["course"] = course
    elif book:
        filters["book"] = book
    else:
        return None

    return Discount.objects.filter(**filters).first()