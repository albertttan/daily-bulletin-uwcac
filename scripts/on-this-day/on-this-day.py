# Legacy code from the Songjiang Daily Bulletin project by Albert Tan
# See https://git.runxiyu.org/sjdb-legacy.git/tree/on_this_day/on_this_day.py


import requests
import re
import datetime
from bs4 import BeautifulSoup

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


for index in range(12):

    month = months[index]
    day = 1
    url = "https://en.m.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/" + month
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    p_elements = soup.find_all("p")

    for p_element in p_elements:

        try: 
            datetime_time = datetime.datetime(2000, index+1, day)
            formatted_time_yearless = datetime_time.strftime("%m-%d")
        except ValueError: 
            break

        if not re.search(
            f'<p><b><a href="/wiki/{month}_\\d+" title="{month} \\d+">{month} \\d+</a></b',
            str(p_element),
        ):
            continue
        div_element = p_element.find_next("div")
        ul_element = div_element.find_next_sibling("ul")
        ul_element_2 = ul_element.find_next("ul")
        p_element_2 = soup.new_tag("p")
        li_contents = [li for li in ul_element_2.find_all("li")]

        for li in li_contents:
            p_element_2.append(li)

        result = (
            str(p_element).replace("/wiki", "https://en.wikipedia.org/wiki")
            + str(ul_element).replace("/wiki", "https://en.wikipedia.org/wiki")
            + "\n"
            + str(p_element_2)
            .replace("</li><li>", "; ")
            .replace("<li>", "<b>Births and Deaths: </b>")
            .replace("</li>", "")
            .replace("/wiki", "https://en.wikipedia.org/wiki")
        )
        result = re.sub(r" <i>.*?icture.*?</i>", "", result)

        with open(formatted_time_yearless + ".html", "w") as file:
            file.write(result)
            file.close()
            day += 1
