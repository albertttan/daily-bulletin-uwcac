import re
import csv


# Input and setup

with open("contacts-raw.txt", "r", encoding="utf-8") as file:
    lines = list(map(str.strip, file.readlines()))
    
students = set()
teachers = set()


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
            students.add((name, email))
        else:
            teachers.add((name, email))


# Output CSV files

def write_csv(file_path, data):
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email"])
        writer.writerows(sorted(data))

write_csv('contacts-students.csv', students)
write_csv('contacts-teachers.csv', teachers)
