import json
import datetime
from itertools import cycle, islice
from typing import Optional


# Parameters

start_date = datetime.date(2025, 3, 6)
end_date = datetime.date(2025, 6, 13)
START_MENU_WEEK = "C"
START_CODES = "EFGA"


# Define rotation and exceptions

menu_weeks_list = ["A", "B", "C"]
codes_sets_list = ["ABCD", "EFGA", "BCDE", "FGAB", "CDEF", "GABC", "DEFG"]
with open("exceptions.json", "r") as file:
    exceptions = json.load(file)
    exceptions_days = exceptions


# Define start values

data = {}
menu_weeks = islice(
    cycle(menu_weeks_list), menu_weeks_list.index(START_MENU_WEEK), None
)
codes_sets = islice(cycle(codes_sets_list), codes_sets_list.index(START_CODES), None)
date = start_date


# Loop through the selected dates

while date <= end_date:
    iso_date = date.isoformat()

    # Assign weekday
    weekday_int = date.weekday() + 1
    weekday_str = date.strftime("%A")

    # Assign codes
    codes: Optional[str] = None
    if weekday_int <= 5 and iso_date not in exceptions["days"]:
        codes = next(codes_sets)

    # Assign menu_week
    if (weekday_int == 1 or date == start_date) and iso_date not in exceptions["weeks"]:
        menu_week = next(menu_weeks)

    date += datetime.timedelta(days=1)
    data[iso_date] = {
        "iso": iso_date,
        "weekday_int": str(weekday_int),
        "weekday_str": weekday_str,
        "codes": codes,
        "menu_week": menu_week,
    }


# Save to JSON file

with open("cycles.json", "w") as file:
    json.dump(data, file, indent=4)
