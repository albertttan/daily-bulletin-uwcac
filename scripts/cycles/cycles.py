import json
import datetime
from itertools import cycle, islice
from typing import Optional


# Parameters

start_date = datetime.date(2025, 9, 23)
end_date = datetime.date(2025, 10, 24)
START_MENU = "A"
START_CODE = "C"


# Define rotation and exceptions

menu_alphabet = list("ABC")
code_alphabet = list("ABCDEFG")

with open("exceptions.json", "r") as file:
    exceptions = json.load(file)


# Initialize values

data = {}
date = start_date
menu_sequence = islice(cycle(menu_alphabet), menu_alphabet.index(START_MENU), None)
code_sequence = islice(cycle(code_alphabet), code_alphabet.index(START_CODE), None)


# Helper: Get the next n codes from the iterator

def get_next_codes(n, code_iter):
    return ''.join(next(code_iter) for _ in range(n))


# Loop through dates

while date <= end_date:
    iso_date = date.isoformat()

    # Assign weekdays
    weekday_int = date.weekday() + 1  # Monday = 1
    weekday_str = date.strftime("%A")

    # Assign codes
    codes: Optional[str] = None
    if weekday_int <= 5 and iso_date not in exceptions["days"]:
        if weekday_int == 2:  # Tues–Thurs: 5 codes
            codes = get_next_codes(4, code_sequence)
        else:  # Mon/Fri: 4 codes
            codes = get_next_codes(5, code_sequence)
            skip = get_next_codes(6, code_sequence)

    # Assign menus
    if (weekday_int == 1 or date == start_date) and iso_date not in exceptions["weeks"]:
        menu_week = next(menu_sequence)

    data[iso_date] = {
        "iso": iso_date,
        "weekday_int": str(weekday_int),
        "weekday_str": weekday_str,
        "codes": codes,
        "menu_week": menu_week,
    }

    date += datetime.timedelta(days=1)


# Save to JSON

with open("cycles.json", "w") as file:
    json.dump(data, file, indent=4)
