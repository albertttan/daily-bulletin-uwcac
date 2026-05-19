import re
import json


# Input and setup

with open("contacts-raw-2026.txt", "r", encoding="utf-8") as file:
    lines = list(map(str.strip, file.readlines()))

students = ""
teachers = ""


# Loop through raw contacts file

i = 0
while i < len(lines):

    # Skip empty lines, drag indicators, and sidebar lines
    if lines[i] in ["", "drag_indicator", "Skip to main content", 
        "Press question mark to see available shortcut keys",
        "person", "Contacts", "domain", "Directory",
        "history", "Frequent", "archive", "Other contacts",
        "Fix & manage", "handyman", "Merge & fix", "download",
        "Import", "delete", "Trash", "Labels", "Directory"]\
        or re.match(r"\(\d*\)", lines[i]):
        i += 1
        continue

    # Skip phone numbers
    if re.match(r".*\d", lines[i]):
        i += 1
        continue

    # Skip additional teacher info lines
    i += 1
    while i < len(lines) and not re.match(r"\S+@uwcatlantic\.org", lines[i]):
        i += 1

    # Read and record names and emails
    if i < len(lines):
        if re.match(r"a\d{2}\w{3,4}@uwcatlantic\.org", lines[i]):
            students += f"{lines[i-1]} <{lines[i]}>,\n"
        else:
            teachers += f"{lines[i-1]} <{lines[i]}>,\n"
        i += 1


# Save to JSON files

with open("contacts-students.txt", "w") as file:
    file.write(students[:-2])
with open("contacts-teachers.txt", "w") as file:
    file.write(teachers[:-2])
