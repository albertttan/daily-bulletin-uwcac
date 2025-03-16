import datetime
import requests
from bs4 import BeautifulSoup


def retrieve_history(date_iso):

    # Retrieve page
    selected_date = datetime.date.fromisoformat(date_iso)
    url = (
        "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
        + selected_date.strftime("%B")
    )
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    date_name = soup.find_all("a", title=selected_date.strftime("%B %-d"))[1].parent.parent
    date_history = date_name.find_next("ul").find_all("li")

    # Clean results
    for element in date_history:
        for link in element.find_all("a"):
            link["href"] = "https://en.wikipedia.org" + link["href"]
        for italics in element.find_all("i"):
            if italics.text.startswith("("):
                italics.decompose()

    return [date_history[0], date_history[-1]]


def retrieve_news():

    # Retrieve page
    url = "https://apnews.com/world-news"
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    output = []

    # Locate headings
    for element in soup.find_all("div", class_="PagePromo-content")[:3]:
        heading = element.find("h3")
        output.append(heading.find("a"))
    
    # Clean results
    for element in output:
        del element["class"]
        element.find("span").unwrap()

    return output
