import os
import json
import base64
import datetime
from bs4 import BeautifulSoup


def encode_image(path):
	filetype = path.split(".")[-1].lower()
	if filetype == "jpg": 
		filetype = "jpeg"
	elif filetype == "svg": 
		filetype = "svg+xml"
	with open(path, "rb") as file: 
		raw = file.read()
	encoded = base64.b64encode(raw).decode("utf-8", "surrogateescape")
	encoded = f"data:image/{filetype};base64," + encoded
	return encoded


def compile_email(date_iso, contacts, html): 

	# Load relevant files
	with open(f"contacts/{contacts}.json") as file: 
		recipients = ', '.join(f'{k} <{v}>' for k, v in json.load(file).items())
	with open("../static/styles.css") as file: 
		css = file.read()
	soup = BeautifulSoup(html, "html.parser")

	# Attach CSS
	soup.find("link").decompose()
	style = soup.new_tag("style")
	style.string = css
	soup.head.append(style)

	# Attach images
	imgs = soup.find_all("img")
	for img in imgs: 
		img["src"] = encode_image(img["src"])

	# Encode HTML
	encoded_html = base64.b64encode(str(soup).encode("utf-8")).decode("utf-8", "surrogateescape")

	# Output
	with open(f"../emails/Daily Bulletin {date_iso}.eml", "w") as file: 
		file.write(f'''Subject: Daily Bulletin {date_iso}
From: WellCo Daily Bulletin <wellco@uwcatlantic.org>
Cc: Albert Tan <a24ytan@uwcatlantic.org>, Jane Xu <a24jxu@uwcatlantic.org>, Adonis Rodulfo <a24arod@uwcatlantic.org>
Bcc: {recipients}
Content-Transfer-Encoding: base64
Content-Type: text/html; charset=UTF-8

{encoded_html}
''')


def update_pages(date_iso): 
	
	with open(f"../pages/latest.html", "r+") as file: 
		soup = BeautifulSoup(file.read(), "html.parser")
		soup.find("meta")["content"] = f'0; url="{date_iso}.html"'
		file.seek(0)
		file.write(str(soup))
		file.truncate()

	with open(f"../pages/index.html", "r+") as file:
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

update_pages("2025-03-03")