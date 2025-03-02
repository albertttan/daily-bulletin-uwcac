import os
import json
import datetime
import markdown as md
from jinja2 import Environment, FileSystemLoader
from compile import compile_email, update_pages
from retrieve import retrieve_history, retrieve_news


# Parameters

def render_html(date_iso=None, recipients="contacts-trial"):

	# Initialization

	if date_iso:
		date = [
			datetime.date.fromisoformat(date_iso),
			datetime.date.fromisoformat(date_iso) + datetime.timedelta(days=1)
		]
	else: 
		date = [
			datetime.date.today() + datetime.timedelta(days=1),
			datetime.date.today() + datetime.timedelta(days=2)
		]
		date_iso = date[0].isoformat()

	env = Environment(loader=FileSystemLoader("."))
	template = env.get_template("template.html")
	print("Processed date and template...")


	# Cycles

	with open("cycles/cycles.json") as file:
		cycles = json.load(file)

	cycle_info = [
		cycles[date_iso],
		cycles[date[1].isoformat()]
	]
	print("Processed cycle information...")


	# Inspirations

	with open(f"inspirations/{date_iso}.md") as file:
		inspirations = md.markdown(file.read(), output_format="html")

	inspirations = inspirations.replace("<p><strong>", '<p class="note">')\
							   .replace("</strong></p>", "</p>")
	print("Processed inspirations...")


	# Exams

	if os.path.isfile(f"exams/{date_iso}.html"):
		with open(f"exams/{date_iso}.html") as file: 
			exam_info = file.read()
	else: 
		exam_info = None
	print("Processed exam information...")


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
	print("Processed menu information...")


	# Events

	with open("events/events.json") as file:
		events = json.load(file)

	try: 
		event_info = [
			events[date_iso],
			events[date[1].isoformat()]
		]
	except KeyError:
		event_info = [
			events[date_iso],
			{}
		]

	event_len = [len(event_info[0]), len(event_info[1])]
	print("Processed event information...")


	# On This Day / In the News

	history_info = retrieve_history(date_iso)
	news_info = retrieve_news()
	print("Processed On This Day and In the News...")


	# Render and save page

	output = template.render(
		cycle_info=cycle_info,
		inspirations=inspirations,
		exam_info=exam_info,
		menu_info=menu_info,
		menu_len=menu_len,
		event_info=event_info,
		event_len=event_len,
		history_info=history_info,
		news_info=news_info
	)
	with open(f"../pages/{date_iso}.html", "w") as file: 
		file.write(output)
	print("Render successful!")


	# Manual confirmation to proceed

	action = ""
	while not action:
		action = input("[V]iew / [E]dit / [Q]uit / [C]onfirm: ")
		if action.lower() == "c" or action.lower() == "confirm":
			continue
		elif action.lower() == "v" or action.lower() == "view": 
			os.system(f"open -a 'Firefox' ../pages/{date_iso}.html")
		elif action.lower() == "e" or action.lower() == "edit": 
			os.system(f"open -a 'Sublime Text' ../pages/{date_iso}.html")
		elif action.lower() == "q" or action.lower() == "quit":
			quit()
		action = ""


	# Compile email & upload page

	with open(f"../pages/{date_iso}.html") as file: 
		output = file.read()

	compile_email(date_iso, recipients, output)
	os.system(f"open -a 'Mail' ../emails/Daily\ Bulletin\ {date_iso}.eml")

	update_pages(date_iso)

	os.chdir("..")
	os.system("git add .")
	os.system(f"git commit -m 'Reuploaded Daily Bulletin {date_iso}'")
	os.system("git push origin main")


if __name__ == "__main__": 
	render_html()
