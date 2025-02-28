import os
import json
import datetime
import markdown as md
from jinja2 import Environment, FileSystemLoader
from compile import compile_email


# Parameters

selected_date = False


# Initialization

if selected_date:
	date = [
		datetime.date(selected_date[0], selected_date[1], selected_date[2]),
		datetime.date(selected_date[0], selected_date[1], selected_date[2]) + datetime.timedelta(days=1)
	]
else: 
	date = [
		datetime.date.today() + datetime.timedelta(days=1),
		datetime.date.today() + datetime.timedelta(days=2)
	]

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")


# Cycles

with open("cycles/cycles.json") as file:
	cycles = json.load(file)

cycle_info = [
	cycles[date[0].isoformat()],
	cycles[date[1].isoformat()]
]


# Inspirations

with open(f"inspirations/{date[0].isoformat()}.md") as file:
	inspirations = md.markdown(file.read())


# Exams

if os.path.isfile(f"exams/{date[0].isoformat()}.html"):
	with open(f"exams/{date[0].isoformat()}.html") as file: 
		exam_info = file.read()
else: 
	exam_info = None


# Menus

with open("menus/menu.json") as file:
	menus = json.load(file)

try:
	menu_info = [
		menus[cycle_info[0]["menu_week"] + cycle_info[0]["weekday_int"]],
		menus[cycle_info[1]["menu_week"] + cycle_info[1]["weekday_int"]]
	]
except KeyError:
	menu_info = [
		menus[cycle_info[0]["menu_week"] + cycle_info[0]["weekday_int"]],
		{}
	]

menu_len = [sum(1 for i in menu_info[0].values() if i), sum(1 for i in menu_info[1].values() if i)]


# Events

with open("events/events.json") as file:
	events = json.load(file)

try: 
	event_info = [
		events[date[0].isoformat()],
		events[date[1].isoformat()]
	]
except KeyError:
	event_info = [
		events[date[0].isoformat()],
		{}
	]

event_len = [len(event_info[0]), len(event_info[1])]


# On This Day

with open(f"on-this-day/{date[0].isoformat()[-5:]}.html") as file:
	on_this_day = file.read()


# In the News

os.chdir("in-the-news")
os.system("python3 in-the-news.py")
os.chdir("..")
with open(f"in-the-news/latest.html") as file:
	in_the_news = file.read()


# Render template

output = template.render(
	cycle_info=cycle_info,
	inspirations=inspirations,
	exam_info=exam_info,
	menu_info=menu_info,
	menu_len=menu_len,
	event_info=event_info,
	event_len=event_len,
	on_this_day=on_this_day,
	in_the_news=in_the_news
)

with open(f"../pages/{date[0].isoformat()}.html", "w") as file: 
	file.write(output)
with open(f"../pages/latest.html", "w") as file: 
	file.write(output)

compile_email(date[0].isoformat(), "contacts-example", output)
