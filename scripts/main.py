import os
import sys
import json
import datetime
import subprocess
import markdown as md
from jinja2 import Environment, FileSystemLoader
from compile import compile_email, update_pages
from retrieve import retrieve_history, retrieve_news


def render_html(date):

    # Initialization

    date_iso = date[0].isoformat()
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    print("Processed date and template...", file=sys.stderr)

    # Cycles

    with open("cycles/cycles.json") as file:
        cycles = json.load(file)

    cycle_info = [cycles[date_iso], cycles[date[1].isoformat()]]
    print("Processed cycle information...", file=sys.stderr)

    # Inspirations

    with open(f"inspirations/{date_iso}.md") as file:
        inspirations = md.markdown(file.read(), output_format="html")

    inspirations = inspirations.replace(
        "<p><strong>", '<p class="note">'
    ).replace(
        "</strong></p>", "</p>"
    )
    print("Processed inspirations...", file=sys.stderr)

    # Exams

    if os.path.isfile(f"exams/{date_iso}.html"):
        with open(f"exams/{date_iso}.html") as file:
            exam_info = file.read()
    else:
        exam_info = None
    print("Processed exam information...", file=sys.stderr)

    # Menus

    with open("menus/menu.json") as file:
        menus = json.load(file)

    try:
        menu_info = [
            menus[cycle_info[0]["menu_week"] + cycle_info[0]["weekday_int"]],
            menus[cycle_info[1]["menu_week"] + cycle_info[1]["weekday_int"]],
        ]
    except KeyError:
        menu_info = [
            menus[cycle_info[0]["menu_week"] + cycle_info[0]["weekday_int"]],
            {},
        ]

    menu_len = [
        sum(1 for i in menu_info[0].values() if i),
        sum(1 for i in menu_info[1].values() if i),
    ]
    print("Processed menu information...", file=sys.stderr)

    # Events

    with open("events/events.json") as file:
        events = json.load(file)

    try:
        event_info = [events[date_iso], events[date[1].isoformat()]]
    except KeyError:
        event_info = [events[date_iso], {}]

    event_len = [len(event_info[0]), len(event_info[1])]
    print("Processed event information...", file=sys.stderr)

    # On This Day / In the News

    history_info = retrieve_history(date_iso)
    news_info = retrieve_news()
    print("Processed Today in History and News...", file=sys.stderr)

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
        news_info=news_info,
    )

    output_path = f"../pages/{date_iso}.html"
    with open(output_path, "w") as file:
        file.write(output)
    print("Render successful!", file=sys.stderr)

    return news_info[-1]


def main(date_iso=None, stop_render=None, recipients=None):

    if not stop_render: 

        if date_iso:
            date = [
                datetime.date.fromisoformat(date_iso),
                datetime.date.fromisoformat(date_iso) + datetime.timedelta(days=1),
            ]
        else:
            date = [
                datetime.date.today() + datetime.timedelta(days=1),
                datetime.date.today() + datetime.timedelta(days=2),
            ]
            date_iso = date[0].isoformat()

        # Manual confirmation to proceed
        news_timestamp = render_html(date)

        output_path = f"../pages/{date_iso}.html"
        action = ""
        while not action:
            action = input("[V]iew / [E]dit / [R]erun / [Q]uit / [C]onfirm: ")
            if action.lower() == "c" or action.lower() == "confirm":
                continue
            if action.lower() == "v" or action.lower() == "view":
                subprocess.run(["open", "-a", "Firefox", output_path], check=True)
            elif action.lower() == "e" or action.lower() == "edit":
                subprocess.run(["open", "-a", "Sublime Text", output_path], check=True)
            elif action.lower() == "r" or action.lower() == "rerun": 
                news_timestamp = render_html(date)
            elif action.lower() == "q" or action.lower() == "quit":
                sys.exit(0)
            action = ""

        if news_timestamp: 
            with open("google-auth/timestamp.txt", "w") as file:
                file.write(news_timestamp)

        with open(f"../pages/{date_iso}.html") as file:
            output = file.read()

    # Compile email & upload page

    if recipients: 
        compile_email(date_iso, recipients, output)
        subprocess.run(
            ["open", "-a", "Mail", f"../emails/Daily Bulletin {date_iso}.eml"], check=True
        )

    update_pages(date_iso)

    os.system("git add ..")
    subprocess.run(["git", "commit", "-m", f"Daily Bulletin {date_iso}"], check=True)
    os.system("git push origin main")


if __name__ == "__main__":
    main()
