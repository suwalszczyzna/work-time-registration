import holidays
from datetime import date
import pandas as pd


def is_weekend(day: date):
    return date.weekday(day) in [5, 6]


def number_of_business_days_without_holidays(date_from: date, date_to: date) -> int:
    if date_from > date_to:
        raise ValueError('date_from should be earlier than date_to')

    result = 0
    for day in pd.date_range(date_from, date_to):
        if day not in holidays.PL() and not is_weekend(day):
            print(date.weekday(day))
            result += 1
    return result
