"""Routes related to AdressData database colection."""
from flask import request, jsonify, Response, Blueprint
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

from flaskr.models.db import db
from flaskr.models.adress_data import AdressData


adress_data_blueprint = Blueprint("adress_data_blueprint", __name__)


def scrape_words(url: str):
    """Scrape words from given url."""
    pass


def scrape_data(url: str, nesting_lvl: str, wiki: bool):
    """Runs scraping on given url and nested urls."""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    links = []
    if wiki:
        for link in soup.findAll('a', attrs={'href': re.compile("^/wiki/")}):
            links.append(link.get('href'))
    else:
        for link in soup.findAll('a', attrs={'href': re.compile("^(http|https)://")}):
            links.append(link.get('href'))

    return links


@adress_data_blueprint.route("/")
def hello_world() -> str:
    """Endpoint test route."""
    return "<p>Hello, World!</p>"


@adress_data_blueprint.route("/test-db")
def test_db() -> str:
    """Endpoint to test databse connection."""
    colection = db[f"{AdressData.colection_name}"]
    adress_data = AdressData("fasfas", ["fasdf", "fasdf", "fasdf"])
    result = colection.insert_one(adress_data.__dict__)
    colection.delete_one({'_id': result.inserted_id})
    return f"<p>Inserted id: {result.inserted_id}</p>"


@adress_data_blueprint.route("/scrape-url")
def scrape_url() -> str:
    """Endpoint for scraping words from given url and nested urls."""
    url = "https://pl.wikipedia.org/wiki/Kr%C3%B3l_Artur"
    nesting_lvl = 1
    wiki = False

    data = scrape_data(url, nesting_lvl, wiki)

    return str(data)
