import datetime
import math

def convert_str_to_date(item: dict) -> dict:
    date_format = "%d.%m.%Y"
    result = {}
    keys = ['date_of_dispatch', 'arrival_date']
    for key, value in item.items():
        if value is None:
            result[key] = None
        elif key in keys:
            result[key] = datetime.datetime.strptime(value, date_format).date()
        else:
            result[key] = value
    return result



def convert_nan_to_none(item: dict) -> dict:
    result = {}
    for key, value in item.items():
        if isinstance(value, float) and math.isnan(value):
            result[key] = None
        else:
            result[key] = value
    return result


