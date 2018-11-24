import datetime


def get_date_for_display(date: datetime.datetime):
    today = datetime.date.today()
    is_same_day = date.day == today.day
    is_same_year = date.year == today.year

    if is_same_day:
        return str(date.hour) + "H" + str(date.minute)

    if is_same_year:
        return str(date.day) + " " + date.strftime("%B")

    return date.strftime("%B") + " " + str(date.year)
