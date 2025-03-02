import requests
from bs4 import BeautifulSoup


def retrieve_news():

    url = "https://apnews.com"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    output = []
    for element in soup.find_all("div", class_="PageListStandardE-leadPromo-info"): 
        output.append(element.find("a"))

    for element in output: 
        del element["class"]
        element.find("span").unwrap()

    return output[:2]
