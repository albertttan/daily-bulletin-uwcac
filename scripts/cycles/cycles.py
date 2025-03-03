import json
import datetime
from itertools import cycle, islice
from typing import Optional


# Parameters

start_date = datetime.date(2025, 2, 28)
end_date = datetime.date(2025, 6, 13)
start_menu_week = "B"
start_codes = "GABC"


# Define rotation and exceptions

menu_weeks_list = ["A", "B", "C"]
codes_sets_list = ["ABCD", "BCDE", "CDEF", "DEFG", "EFGA", "FGAB", "GABC"]
with open("exceptions.txt", "r") as file:
    exceptions = list(map(str.strip, file.readlines()))


# Define start values

data = {}
menu_weeks = islice(cycle(menu_weeks_list), menu_weeks_list.index(start_menu_week), None)
codes_sets = islice(cycle(codes_sets_list), codes_sets_list.index(start_codes), None)
date = start_date


# Loop through the selected dates

while date <= end_date:
    iso_date = date.isoformat()

    # Assign weekday
    weekday_int = date.weekday() + 1
    weekday_str = date.strftime("%A")

    # Assign codes
    codes: Optional[str] = None
    if weekday_int <= 5 and iso_date not in exceptions:
        codes = next(codes_sets)
    else:
        codes = None

    # Assign menu_week
    if weekday_int == 1 or date == start_date:
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

with open("cycles.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
