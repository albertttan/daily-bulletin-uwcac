import os
import json
import base64
import random
import requests
from tkinter import Tk
from bs4 import BeautifulSoup


def encode_image(path):
    filetype = path.split(".")[-1].lower()

    # Check file type
    if filetype == "jpg":
        filetype = "jpeg"
    elif filetype == "svg":
        filetype = "svg+xml"

    # Load image
    if path.startswith("http://") or path.startswith("https://"):
        response = requests.get(path, timeout=30)
        response.raise_for_status()
        raw = response.content
    elif os.path.isfile(path):
        with open(path, "rb") as file:
            raw = file.read()
    else:
        raise FileNotFoundError(f"No such file or URL: '{path}'")

    # Encode image
    encoded = base64.b64encode(raw).decode("utf-8", "surrogateescape")
    encoded = f"data:image/{filetype};base64," + encoded
    return encoded


def compile_email(date_iso):

    with open(f"contacts/contacts.txt") as file:
        recipients = file.read()
    with open(f"cycles/cycles.json") as file:
        cycles = json.load(file)
        weekday_str = cycles[date_iso]["weekday_str"]

    to = "direct recipient|Albert Tan <a24ytan@uwcatlantic.org>"
    bcc = f"bcc recipients|{recipients}"
    subject = f"email subject|Daily Bulletin {date_iso}"
    link = f"page URL|https://albertttan.github.io/daily-bulletin-uwcac/pages/{date_iso}.html"

    content = "email contents|"
    content += random.choice(["Hi ", "Hi ", "Hello ", "Greetings " ])
    content += random.choice(["all,\n\n", "all,\n\n", "everyone,\n\n", "Atlantic College,\n\n"])
    content += random.choice(["", "", "Good morning! ", f"Happy {weekday_str}! "])
    content += random.choice([
        "Here's today's Daily Bulletin!\n\n",
        "Here's today's Daily Bulletin!\n\n",
        "Here's today's bulletin!\n\n",
        "Please check today's Daily Bulletin.\n\n"
    ])
    content += random.choice([
        "Lots of wellbeing love,\n",
        "Lots of wellbeing love,\n",
        "Thanks,\n",
        "Have a great day,\n"
    ])
    content += "WellCo and Albert"

    for info in [to, bcc, subject, content, link]:
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(info.split("|")[1])
        r.update()
        r.destroy()
        input(f"Copied {info.split("|")[0]} to clipboard...")


def update_pages(date_iso):

    with open("../pages/latest.html", "r+") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        soup.find("meta")["content"] = f'0; url="{date_iso}.html"'
        file.seek(0)
        file.write(str(soup))
        file.truncate()

    with open("../pages/index.html", "r+") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        if soup.find("a", href=f"{date_iso}.html"):
            return
        new_entry = soup.new_tag("li")
        new_link = soup.new_tag("a", href=f"{date_iso}.html")
        new_link.string = date_iso
        new_entry.append(new_link)
        soup.find("ul").insert(0, new_entry)
        file.seek(0)
        file.write(str(soup))
        file.truncate()
