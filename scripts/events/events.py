import json
import datetime
import pandas as pd


# Initialization

df = pd.read_excel("events.xlsx", sheet_name="10-1611", skiprows=2)[
    ["Unnamed: 0", "When", "What", "Where"]
]
df.rename(columns={"Unnamed: 0": "Day"}, inplace=True)
date = ""

with open("events.json") as file:
    data = json.load(file)


# Formatting


def title_case(s):
    if not isinstance(s, str):
        return s

    exceptions = [
        "and", "as", "but", "for", "if", "nor", 
        "or", "so", "yet", "a", "an", "the",
        "as", "at", "by", "for", "in", "of", 
        "off", "on", "per", "to", "up", "via",
    ]  # https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case
    words = s.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in exceptions:
            result.append(word[0].upper() + word[1:] if word[0].islower() else word)
        else:
            result.append(word.lower())
    return " ".join(result).replace("Drop in", "Drop-in").replace("WellCo", "WellCo ☀️")


df = df.map(title_case)


# Iterating through rows

for index in df.index:
    row = df.loc[index]
    if isinstance(row["Day"], datetime.datetime):
        if date:
            data[date] = entry_day
        date = row["Day"].date().isoformat()
        entry_day = []
    if not pd.isna(row["When"]):
        if row["When"][0] == "0" or row["When"][0] == "1":
            time = row["When"][:5] + "–" + row["When"][-5:]
        else:
            time = "0" + row["When"][:4] + "–" + row["When"][-5:]
        entry_day.append({"when": time, "what": row["What"], "where": row["Where"]})
    data[date] = entry_day


# Save to JSON file

with open("events.json", "w") as file:
    json.dump(data, file, indent=4)
