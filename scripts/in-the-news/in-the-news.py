# Legacy code from the Songjiang Daily Bulletin project by Albert Tan
# See https://git.runxiyu.org/sjdb-legacy.git/tree/on_this_day/on_this_day.py


import requests
import re
import copy
import datetime
from bs4 import BeautifulSoup


url = "https://en.m.wikipedia.org/wiki/Main_Page"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

h2_element = soup.find("h2", id="mp-itn-h2")
ul_element = h2_element.find_next("ul")
ul_element_2 = ul_element.find_next("ul")
div_element = ul_element_2.find_next("div")
ul_element_3 = div_element.find_next("ul")

p_element_2 = soup.new_tag("p")
p_element_3 = soup.new_tag("p")
li_contents_2 = [li for li in ul_element_2.find_all("li")]
li_contents_3 = [li for li in ul_element_3.find_all("li")]
skip = False
for li in li_contents_2:
    if skip:
        skip = False
        continue
    if li.find("ul"):
        new_li = copy.deepcopy(li)
        new_li.find("ul").decompose()
        p_element_2.append(new_li)
        skip = True
    else:
        p_element_2.append(li)
for li in li_contents_3:
    if skip:
        skip = False
        continue
    if li.find("ul"):
        new_li = copy.deepcopy(li)
        new_li.find("ul").decompose()
        p_element_3.append(new_li)
        skip = True
    else:
        p_element_3.append(li)

result = (
    str(ul_element).replace("/wiki", "https://en.wikipedia.org/wiki")
    + str(p_element_2)
    .replace("</li><li>", "; ")
    .replace("<li>", "<b>Ongoing: </b>")
    .replace("</li>", "")
    .replace("\n;", ";")
    .replace("/wiki", "https://en.wikipedia.org/wiki")
    .replace("</p>", "<br>")
    + str(p_element_3)
    .replace("</li><li>", "; ")
    .replace("<li>", "<b>Recent deaths: </b>")
    .replace("</li>", "")
    .replace("\n;", ";")
    .replace("/wiki", "https://en.wikipedia.org/wiki")
    .replace("<p>", "")
)
result = re.sub(r" <i>\(.*?\)</i>", "", result)

with open("latest.html", 'r') as file:
    existing_content = file.read()

if existing_content != result:
    datetime_time = datetime.datetime.today() + datetime.timedelta(days=-1)
    formatted_time = datetime_time.strftime("%Y-%m-%d")
    new_filename = formatted_time + ".html"

    with open(new_filename, "w") as file:
        file.write(existing_content)
        file.close()

    with open("latest.html", "w") as file:
        file.write(result)
        file.close()
