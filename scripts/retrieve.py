import datetime
import requests
from bs4 import BeautifulSoup


def retrieve_history(date_iso):

    selected_date = datetime.date.fromisoformat(date_iso)
    url = (
        "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
        + selected_date.strftime("%B")
    )
    soup = BeautifulSoup(requests.get(url, timeout=30).text, "html.parser")
    date_name = soup.find_all("a", title=selected_date.strftime("%B %-d"))[
        1
    ].parent.parent
    date_history = date_name.find_next("ul").find_all("li")

    for element in date_history:
        for link in element.find_all("a"):
            link["href"] = "https://en.wikipedia.org" + link["href"]
        for italics in element.find_all("i"):
            if italics.text.startswith("("):
                italics.decompose()

    return [date_history[0], date_history[-1]]


def retrieve_news():

    url = "https://apnews.com"
    soup = BeautifulSoup(requests.get(url, timeout=30).text, "html.parser")
    output = []

    for element in soup.find_all("div", class_="PageListStandardE-leadPromo-info"):
        output.append(element.find("a"))
    output = output[:2]

    for element in soup.find("div", class_="PageList-items").find_all(
        "h3", class_="PagePromo-title"
    ):
        output.append(element.find("a"))

    for element in output:
        del element["class"]
        element.find("span").unwrap()

    return output


retrieve_news()
