import datetime


def get_date_for_display(date: datetime.datetime):
    today = datetime.date.today()
    is_same_day = date.day == today.day
    is_same_year = date.year == today.year

    if is_same_day:
        return date.strftime("%H") + "H" + date.strftime("%M")

    if is_same_year:
        return date.strftime("%d") + " " + date.strftime("%B")

    return date.strftime("%B") + " " + date.strftime("%Y")
