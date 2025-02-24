import json
import datetime
from itertools import cycle, islice


# Parameters

start_date = datetime.date(2025, 2, 28)
end_date = datetime.date(2025, 6, 13)
start_menu_week = "B"
start_code_day = "GABC"


# Define rotation and exceptions

menu_weeks = ["A", "B", "C"]
code_days = ["ABCD", "BCDE", "CDEF", "DEFG", "EFGA", "FGAB", "GABC"]
with open("exceptions.txt", "r") as file:
    exceptions = list(map(str.strip, file.readlines()))


# Define start values

data = {}
menu_weeks = islice(cycle(menu_weeks), menu_weeks.index(start_menu_week), None)
code_days = islice(cycle(code_days), code_days.index(start_code_day), None)
date = start_date


# Loop through the selected dates

while date <= end_date:
    iso_date = date.isoformat()
    
    # Assign week_day
    week_day = date.weekday() + 1
    
    # Assign code_day
    if week_day <= 5 and iso_date not in exceptions:
        code_day = next(code_days)
    else:
        code_day = None
    
    # Assign menu_week
    if week_day == 1 or date == start_date:
        menu_week = next(menu_weeks)
    
    date += datetime.timedelta(days=1)
    data[iso_date] = {
        "week_day": week_day,
        "code_day": code_day,
        "menu_week": menu_week,
    }


# Save to JSON file
with open("cycles.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
