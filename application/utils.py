import logging
from datetime import datetime
from collections import Counter
from time import time

import requests
from logger import logger
from lxml import html

from application.db import Database


def get_tag_count_with_timer(url, domain):
    tags_dict, elapsed = timer(get_count, url, domain, True, True)
    return tags_dict, elapsed


def get_from_db(domain):
    db = Database()
    entry, elapsed = timer(db.fetch, domain)
    return entry, elapsed


def get_count(url, domain, log_to_file=True, log_to_db=True):
    tags_dict = counter(url=url)

    if log_to_file:
        create_log_file(domain=domain, tags_dict=tags_dict)

    if log_to_db:
        db = Database()
        db.insert(site_name=domain, url=url, tags_dict=tags_dict)

    return tags_dict


def timer(func, *args):
    start = time()
    returns = func(*args)
    done = time()
    elapsed = str(done - start)[0:4]

    return returns, elapsed


def format_url(url):
    """ Форматирование url """
    if not url.startswith('http'):
        url = 'http://' + url

    return url


def counter(url):
    # Получение html
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Поиск всех тегов
    all_elms = tree.cssselect('*')
    all_tags = [x.tag for x in all_elms]
    tags_dict = dict(Counter(all_tags))

    return tags_dict


def create_log_file(domain, tags_dict):
    now = datetime.now()
    date_time = now.strftime("%m.%d.%Y_%H-%M_")
    filename = 'logs/' + date_time + domain + '.log'
    mode = "w"
    handler = logging.FileHandler(filename=filename, mode=mode)
    logger.addHandler(handler)

    for tag in tags_dict:
        logger.info(f'{tag}: {tags_dict[tag]}')

    handler.close()
