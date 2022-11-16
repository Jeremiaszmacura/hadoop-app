"""Routes related to AdressData database colection."""
import requests
from flask import Blueprint, request, render_template
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re

from flaskr.models.db import db
from flaskr.models.adress_data import AdressData


adress_data_blueprint = Blueprint("adress_data_blueprint", __name__)


def scrape_words(soup) -> str:
    """Scrape words from given url. Returns word list."""
    wordlist = []
    for each_text in soup.findAll(text=True):
        content = each_text.text
        words = content.lower().split()
        for each_word in words:
            if re.match("^[a-zA-Z]*$", each_word):
                wordlist.append(each_word)
    
    return wordlist


def scrape_data(url: str, wiki: bool) -> AdressData:
    """Runs scraping on given url and nested urls."""
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    wordlist = scrape_words(soup)
    adress_data = AdressData(url, words=wordlist)
    if wiki:
        for link in soup.findAll('a', attrs={'href': re.compile("^/en(.*)/wiki/")}):
            adress_data.nested_adresses.append(link.get('href'))
    else:
        for link in soup.findAll('a', attrs={'href': re.compile("^(http|https)://")}):
            adress_data.nested_adresses.append(link.get('href'))

    return adress_data


@adress_data_blueprint.route("/")
def home() -> str:
    """Endpoint test route."""
    return render_template(
        'home.html',
        title="Scraping Words Tool",
        description="Pass URL and numer of adresses to scrape - nesting from the passed url adress"
    )


@adress_data_blueprint.route("/test-db")
def test_db() -> str:
    """Endpoint to test databse connection."""
    colection = db[f"{AdressData.colection_name}"]
    adress_data = AdressData("fasfas", ["fasdf", "fasdf"], ["fasdf", "fasdf"])
    result = colection.insert_one(adress_data.__dict__)
    colection.delete_one({'_id': result.inserted_id})
    return f"<p>Inserted id: {result.inserted_id}</p>"


@adress_data_blueprint.route("/scrape-url", methods = ['GET', 'POST'])
def scrape_url() -> str:
    """Endpoint for scraping words from given url and nested urls."""
    if request.method == 'POST':
        urls = [request.form['urlAdress']]
        nesting_lvl = int(request.form['nestedNumber'])
        wiki = True if request.form.get('wiki') else False
        nest_iter = 0
        data = []

        while nest_iter < nesting_lvl and len(urls) > nest_iter:
            try:
                data.append(scrape_data(urls[nest_iter], wiki))
                if len(urls) <= nesting_lvl:
                    urls.extend(data[-1].nested_adresses)
                    urls = list(set(urls))
            except UnicodeEncodeError as ex:
                print(f"An error ocured: {ex}")
            except urllib.error.HTTPError as ex:
                print(f"An error ocured: {ex}")
            nest_iter = nest_iter + 1

        return str(f"{urls}, liczba obiektów: {len(data)}")
