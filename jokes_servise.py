from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from conf import PROXY_API_KEY


def pull_the_jokes_list():
    r = requests.get(get_scrapeops_url('https://parade.com/968666/parade/chuck-norris-jokes/'))

    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser')
    bs4_jokes_list = soup.find("ol")
    chunk_norris_jokes_list = [joke.text for joke in bs4_jokes_list]
    return chunk_norris_jokes_list


def get_the_jock_number_i(desired_joke_number):
    if 0 < desired_joke_number <= 101:
        jokes_list = pull_the_jokes_list()
        return jokes_list[desired_joke_number - 1]


def get_scrapeops_url(url):
    payload = {'api_key': PROXY_API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
