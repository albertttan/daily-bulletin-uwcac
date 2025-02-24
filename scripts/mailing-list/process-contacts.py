import re
import json


# Input and setup

with open("contacts-raw.txt", "r", encoding="utf-8") as file:
    lines = list(map(str.strip, file.readlines()))
    
students = {}
teachers = {}


# Loop through raw contacts file

i = 0
while i < len(lines):
    name = lines[i]
        
    # Skip phone numbers
    if re.match(r'.*\d', name):
        i += 1
        continue

    # Skip additional teacher info lines
    i += 1
    while i < len(lines) and not re.match(r'\S+@uwcatlantic\.org', lines[i]):
        i += 1
    
    # Read and record names and emails
    if i < len(lines):
        email = lines[i]
        i += 1
        if re.match(r'a\d{2}\w{3,4}@uwcatlantic\.org', email):
            students[name] = email
        else:
            teachers[name] = email


# Output JSON files

with open("contacts-students.json", 'w') as file:
    json.dump(students, file, indent=4)
with open("contacts-teachers.json", 'w') as file:
    json.dump(teachers, file, indent=4)
