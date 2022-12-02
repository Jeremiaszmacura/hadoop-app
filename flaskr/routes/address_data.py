"""Routes related to AddressData database colection."""
import re
import os
import urllib.request
import urllib.error

import matplotlib
import matplotlib.pyplot as plt
import requests
from flask import Blueprint, request, render_template
from bs4 import BeautifulSoup

from flaskr.models.db import db, db_backup
from flaskr.models.address_data import AddressData


matplotlib.use("Agg")

address_data_blueprint = Blueprint("address_data_blueprint", __name__)


def create_words_len_hist(words_list: list) -> str:
    """Plot histogram of words length occurrences and save to OS."""
    words_len_list = list(map(len, words_list))
    binwidth = 1
    path = "flaskr/static/images/histogram.png"
    if not os.path.exists("path/to/demo_folder"):
        os.makedirs("flaskr/static/images", exist_ok=True)
    if os.path.isfile(path):
        os.remove(path)
    plt.hist(
        words_len_list,
        bins=range(min(words_len_list), max(words_len_list) + binwidth, binwidth),
        facecolor="#2ab0ff",
        edgecolor="#169acf",
        linewidth=1,
    )
    plt.xlabel("Word length")
    plt.ylabel("Occurrences")
    plt.savefig(path)
    return path


def most_common_words(words_occurrences: dict) -> list:
    """Takes list of words and return top 10 common words."""
    return sorted(words_occurrences, key=words_occurrences.get, reverse=True)[:10]


def words_length_median(words_list: list):
    """Calculates the median for word lengths."""
    sorted_words = sorted(words_list, key=len)
    list_length = len(sorted_words)
    index = (list_length - 1) // 2
    if list_length % 2:
        return len(sorted_words[index])
    return (len(sorted_words[index]) + len(sorted_words[index + 1])) / 2.0


def count_words_length_mean(words_list: list):
    """Calculates the average word length."""
    return round(sum(map(len, words_list)) / len(words_list), 4)


def concatenate_words_lists(data: list) -> list:
    """Joins words lists from multpiple AddressData objects into one."""
    words_list = []
    for adress_data in data:
        words_list.extend(adress_data.words)
    return words_list


def count_words_occurrences(words_list: list) -> dict:
    """Count occurrences of each word in scraped data."""
    words_occurrences = {}

    for word in words_list:
        if word in words_occurrences:
            words_occurrences[word] = words_occurrences[word] + 1
        else:
            words_occurrences[word] = 1

    return words_occurrences


def calculate_statistics(data: list) -> dict:
    """Calculate statistics and return as a dictionary."""
    statistics = {}
    words_list = concatenate_words_lists(data)
    statistics["words length mean"] = count_words_length_mean(words_list)
    statistics["words median"] = words_length_median(words_list)
    words_occurrences = count_words_occurrences(words_list)
    statistics["screaped_urls"] = get_scraped_urls(data)
    statistics["most common words"] = most_common_words(words_occurrences)
    statistics["histogram"] = create_words_len_hist(words_list)
    statistics["words occurrences"] = words_occurrences
    return statistics


def dict_to_object_list(data_dict: list) -> list:
    """Convert list of dictionaries into list of objects."""
    data = []

    for dict_item in data_dict:
        address_data = AddressData(
            address=dict_item["address"],
            nested_addresses=dict_item["nested_addresses"],
            words=dict_item["words"],
            encrypted=True,
        )
        data.append(address_data)

    return data


def object_list_to_dict(objects_list: list) -> list:
    """Convert list of objects into list of dictionaries."""
    data_dict = []
    for adress_data in objects_list:
        data_dict.append(adress_data.__dict__)
    return data_dict


def get_scraped_urls(objects_list: list) -> list:
    """Get list of scraped urls."""
    scraped_ruls = []
    for adress_data in objects_list:
        scraped_ruls.append(adress_data.address)
    return scraped_ruls


def scrape_words(soup: BeautifulSoup) -> str:
    """Scrape words from given url. Returns word list."""
    wordlist = []
    for each_text in soup.findAll(text=True):
        content = each_text.text
        words = content.lower().split()
        for each_word in words:
            if re.match("^[a-zA-Z]*$", each_word):
                wordlist.append(each_word)

    return wordlist


def scrape_data(url: str, wiki: bool) -> AddressData:
    """Runs scraping on given url and nested urls."""
    source_code = requests.get(url, timeout=10).text
    soup = BeautifulSoup(source_code, "html.parser")
    wordlist = scrape_words(soup)
    address_data = AddressData(url, words=wordlist)
    if wiki:
        for link in soup.findAll("a", attrs={"href": re.compile("^/en(.*)/wiki/")}):
            address_data.nested_addresses.append(link.get("href"))
    else:
        for link in soup.findAll("a", attrs={"href": re.compile("^(http|https)://")}):
            address_data.nested_addresses.append(link.get("href"))

    return address_data


@address_data_blueprint.route("/")
def home() -> str:
    """Endpoint test route."""
    return render_template(
        "home.html",
        title="Scraping Words Tool",
        description="Pass URL and numer of addresses to scrape - nesting from the passed address",
    )


@address_data_blueprint.route("/test-db")
def test_db() -> str:
    """Endpoint to test databse connection."""
    colection = db[f"{AddressData.colection_name}"]
    address_data = AddressData("fasfas", ["fasdf", "fasdf"], ["fasdf", "fasdf"])
    result = colection.insert_one(address_data.__dict__)
    colection.delete_one({"_id": result.inserted_id})
    return f"<p>Inserted id: {result.inserted_id}</p>"


@address_data_blueprint.route("/about")
def about() -> str:
    """Endpoint for about page."""
    with open("flaskr/static/about.txt", "r", encoding="utf-8") as file:
        description = file.read()
    return render_template(
        "about.html",
        title="How to use Scraping Words Tool",
        description=description,
    )


@address_data_blueprint.route("/scrape-url", methods=['POST'])
def scrape_url() -> str:
    """Endpoint for scraping words from given url and nested urls."""
    urls = [request.form["urlAddress"]]
    nesting_lvl = int(request.form["nestedNumber"])
    wiki = bool(request.form.get("wiki"))
    nest_iter = 0
    data = []

    while nest_iter < nesting_lvl and len(urls) > nest_iter:
        try:
            data.append(scrape_data(urls[nest_iter], wiki))
            if len(urls) <= nesting_lvl:
                urls.extend(data[-1].nested_addresses)
                urls = list(set(urls))
        except UnicodeEncodeError as ex:
            print(f"An error ocured: {ex}")
        except urllib.error.HTTPError as ex:
            print(f"An error ocured: {ex}")
        nest_iter = nest_iter + 1

    collection = db[f"{AddressData.colection_name}"]
    collection_backup = db_backup[f"{AddressData.colection_name}"]

    statistics = calculate_statistics(data)

    for adress_data in data:
        adress_data.encrypt()
    data_dict = object_list_to_dict(data)
    collection.insert_many(data_dict)
    collection_backup.insert_many(data_dict)

    return render_template(
        "result.html",
        title="Scraping result",
        statistics=statistics,
    )


@address_data_blueprint.route("/general-statistics")
def general_statistics() -> str:
    """Endpoint to create sttistics from all scared data."""
    data = []

    collection = db[f"{AddressData.colection_name}"]
    data_dict = list(collection.find({}))

    data = dict_to_object_list(data_dict)
    for adress_data in data:
        adress_data.decrypt()

    statistics = calculate_statistics(data)

    return render_template(
        "result.html",
        title="Scraping result",
        statistics=statistics,
    )
